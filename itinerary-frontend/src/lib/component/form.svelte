<script>
  import { slide } from 'svelte/transition';
  import Button from '$lib/components/ui/button/button.svelte';
  import axios, { all } from 'axios';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  const llmOptions = [
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
  { value: "gpt-3.5-turbo-0125", label: "GPT-3.5 Turbo (Jan 2025)" },
  { value: "gpt-4-turbo", label: "GPT-4 Turbo" },
  { value: "gpt-4o", label: "GPT-4o" },
  { value: "gpt-4o-mini", label: "GPT-4o Mini" }, 
  { value: "gpt-4-0613", label: "GPT-4 (June 2023)" }
];


  const placeTypeOptions = [
    { value: '', label: 'No Priority' },
    { value: 'restaurant', label: 'Restaurant' },
    { value: 'cafe', label: 'Cafe' },
    { value: 'tourist_attraction', label: 'Tourist Attraction' },
    { value: 'natural_feature', label: 'Nature' },
    { value: 'museum', label: 'Museum' },
    { value: 'park', label: 'Park' },
    { value: 'shopping_mall', label: 'Mall' }
];

  const searchRangeOptions = [
      { value: 'all', label: 'All Places' },
      { value: 'nearby', label: 'Nearby Places' }
  ];

  let selectedLlm = llmOptions[0].value;
  let prompt = '';
  let selectedPlaceType = placeTypeOptions[0].value;
  let isLoading = false;
  let isFormVisible = false;
  let searchRange = 'all';
  let radiusKm = 10;
  let place = "";
  let all_place = "";
  let allResults = [];
  let llm_result = "";
 let placeDetails = [];

 let placeinput = "";

  const handleSubmit = async () => {

      
      isLoading = true;
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log({ 
          selectedLlm, 
          prompt, 
          selectedPlaceType,
          searchRange,
          ...(searchRange === 'nearby' && { radiusKm })
      });
      try {
        await function_calling_place();

        if (searchRange === "nearby"){

            console.log("MENGAMBIL NEARBY PLACE")

            const coordinate = await get_coordinate()
            console.log(coordinate.longitude)
            await nearby_place(coordinate)

        }else{
            await google_place_all();

        } 



        await generating_itinerary();
        await fetchAllPlaceDetailsParallel()
        
        dispatch("placeUpdate", { 
          place: place,
          llm_result: llm_result,
          allResults: allResults,
          ids : placeDetails
        });
      } catch (error) {
        console.error('Error during submission:', error);
      } finally {
        isLoading = false;
      }
  };

  async function generating_itinerary() {

      try {
          const response = await axios.post('http://127.0.0.1:8000/generate_itinerary', {

            jumlah_hari: String(place.days),
            jam_mulai: String(place.start_time),
            json_data_tempat: JSON.stringify(allResults), 
            place_type: String(selectedPlaceType),
            model : selectedLlm


          }, {
              headers: {
                  'Content-Type': 'application/json'
              }
          });
          llm_result = response.data;
          console.log(llm_result);
      } catch (error) {
          console.error('Failed to generate AI query:', error);
      }
  }

  async function fetchAllPlaceDetailsParallel() {
    try {
        const placeIds = llm_result.result.flatMap(day => 
            day.schedule.map(item => item.place_id)
        ).filter(id => id);

        placeDetails = await Promise.all(
            placeIds.map(id => detailPlace(id))
        );

        console.log('All place details:', placeDetails);
        return placeDetails;
        
    } catch (error) {
        console.error('Error fetching all places:', error);
        throw error;
    }
}
  
  async function detailPlace(id) {

        try {
            const response = await axios.post('http://127.0.0.1:8000/detail_place', {
                place: id
            });
            console.log(response.data);
            return response.data;
            
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }


  async function google_place_all() {
    try {
        let queryType = "tourist_attraction";
        let token = ""; 

        while (true) {
            const response = await axios.post('http://127.0.0.1:8000/google_place', {
                query: `${queryType} in ${place.location}`,
                token: token 
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            let data = response.data;
            allResults.push(...data.results);

            token = data.token || ""; 

            if (token) {
                console.log(`Menunggu 3 detik sebelum ambil halaman berikutnya (${queryType})...`);
                await new Promise(resolve => setTimeout(resolve, 3000)); 
            } else if (queryType === "tourist_attraction") {
                console.log("Semua tempat wisata sudah diambil, lanjut ke restoran...");
                queryType = "restaurant";
                token = ""; 
            } else {
                break;
            }
        }
''
        console.log("Semua data sudah diambil:", allResults);
    } catch (error) {
        console.error('Failed to fetch places:', error);
    }
}




    async function get_coordinate() {

        const response = await axios.post('http://127.0.0.1:8000/google_coordinate', {
              place : placeinput
          }, {
              headers: {
                  'Content-Type': 'application/json'
              }
          });
        
        let data = response.data

        return data
        
    }

    async function nearby_place(coordinate) {

        let queryType = "tourist_attraction";
        let token = ""; 


        while (true) {
            const response = await axios.post('http://127.0.0.1:8000/google_nearby_place', {

            longitude : String(coordinate.longitude),
            latitude : String(coordinate.latitude),
            type_place : "tourist_attraction",
            radius : radiusKm

          }, {
              headers: {
                  'Content-Type': 'application/json'
              }
          });

            let data = response.data;
            allResults.push(...data.results);

            token = data.token || ""; 

            if (token) {
                console.log(`Menunggu 3 detik sebelum ambil halaman berikutnya (${queryType})...`);
                await new Promise(resolve => setTimeout(resolve, 3000)); 
            } else if (queryType === "tourist_attraction") {
                console.log("Semua tempat wisata sudah diambil, lanjut ke restoran...");
                queryType = "restaurant";
                token = ""; 
            } else {
                break;
            }
        }
    }




  async function function_calling_place() {
      try {
          const response = await axios.post('http://127.0.0.1:8000/function_calling_Place', {
              prompt: prompt,
              model : selectedLlm
          }, {
              headers: {
                  'Content-Type': 'application/json'
              }
          });
          place = response.data;
          console.log(response);
      } catch (error) {
          console.error('Failed to generate AI query:', error);
      }
  }

  const toggleForm = () => {
      isFormVisible = !isFormVisible;
  };
</script>





















<div class="p-6 relative">
  <Button
      on:click={toggleForm}
      class="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-all duration-200 shadow-md hover:shadow-lg"
  >
      {#if !isFormVisible}
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Add New Query
      {:else}
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
          Close Form
      {/if}
  </Button>

  {#if isFormVisible}
      <div
          transition:slide={{ duration: 500 }}
          class="absolute top-20 left-6 right-6 bg-white rounded-xl shadow-lg border border-gray-200 p-6 max-w-2xl"
      >
          <h2 class="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
              New AI Query <span class="text-blue-500">✨</span>
          </h2>

          <form on:submit|preventDefault={handleSubmit} class="space-y-5">
              <!-- LLM Selection -->
              <div class="relative group">
                  <label
                      for="llm"
                      class="block text-sm font-medium text-gray-700 mb-2"
                  >
                      Select Language Model
                  </label>
                  <div class="relative">
                      <select
                          id="llm"
                          bind:value={selectedLlm}
                          class="w-full px-4 py-2.5 bg-white text-gray-800 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 appearance-none transition-all hover:border-blue-400"
                      >
                          {#each llmOptions as option}
                              <option value={option.value}>{option.icon} {option.label}</option>
                          {/each}
                      </select>
                      <div class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                          ▼
                      </div>
                  </div>
              </div>

              <!-- Prompt Input -->
              <div class="relative group">
                  <label
                      for="prompt"
                      class="block text-sm font-medium text-gray-700 mb-2"
                  >
                      Enter Your Prompt
                  </label>
                  <textarea
                      id="prompt"
                      bind:value={prompt}
                      rows="3"
                      placeholder="Describe what you're looking for..."
                      class="w-full px-4 py-2.5 bg-white text-gray-800 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all hover:border-blue-400 placeholder-gray-400"
                  />
              </div>

              <!-- Place Type Selection -->
              <div class="relative group">
                  <label
                      for="placeType"
                      class="block text-sm font-medium text-gray-700 mb-2"
                  >
                      Select Place Type
                  </label>
                  <div class="relative">
                      <select
                          id="placeType"
                          bind:value={selectedPlaceType}
                          class="w-full px-4 py-2.5 bg-white text-gray-800 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 appearance-none transition-all hover:border-blue-400"
                      >
                          {#each placeTypeOptions as option}
                              <option value={option.value}>{option.icon} {option.label}</option>
                          {/each}
                      </select>
                      <div class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                          ▼
                      </div>
                  </div>
              </div>

              <!-- Search Range Selection -->
              <div class="relative group">
                  <label
                      for="searchRange"
                      class="block text-sm font-medium text-gray-700 mb-2"
                  >
                      Search Range
                  </label>
                  <div class="relative">
                      <select
                          id="searchRange"
                          bind:value={searchRange}
                          class="w-full px-4 py-2.5 bg-white text-gray-800 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 appearance-none transition-all hover:border-blue-400"
                      >
                          {#each searchRangeOptions as option}
                              <option value={option.value}>{option.label}</option>
                          {/each}
                      </select>
                      <div class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                          ▼
                      </div>
                  </div>
              </div>

              <!-- Radius Slider (only shows when nearby is selected) -->
              {#if searchRange === 'nearby'}
              <div class="relative group" transition:slide={{ duration: 300 }}>
                  <!-- Range Slider for Radius -->
                  <label
                      for="radius"
                      class="block text-sm font-medium text-gray-700 mb-2"
                  >
                      Search Radius: {radiusKm} km
                  </label>
                  <input
                      type="range"
                      id="radius"
                      bind:value={radiusKm}
                      min="10"
                      max="50"
                      step="1"
                      class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-orange-500"
                  />
                  <div class="flex justify-between text-xs text-gray-500 mt-1 mb-4">
                      <span>10km</span>
                      <span>50km</span>
                  </div>
          
                  <label
                      for="alamat"
                      class="block text-sm font-medium text-gray-700 mb-2"
                  >
                      Address
                  </label>
                  <input
                      type="text"
                      id="alamat"
                      bind:value={placeinput}
                      placeholder="Enter your address"
                      class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
                  />
              </div>
          {/if}

              <!-- Submit Button -->
              <div class="flex gap-3">
                  <Button
                      type="submit"
                      disabled={isLoading}
                      class="flex-1 bg-orange-500 text-white py-2.5 px-6 rounded-lg font-medium transition-all hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-md hover:shadow-lg"
                  >
                      {#if isLoading}
                          <svg
                              class="animate-spin h-5 w-5 text-white"
                              xmlns="http://www.w3.org/2000/svg"
                              fill="none"
                              viewBox="0 0 24 24"
                          >
                              <circle
                                  class="opacity-25"
                                  cx="12"
                                  cy="12"
                                  r="10"
                                  stroke="currentColor"
                                  stroke-width="4"
                              />
                              <path
                                  class="opacity-75"
                                  fill="currentColor"
                                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                              />
                          </svg>
                      {/if}
                      {isLoading ? 'Processing...' : 'Generate'}
                  </Button>
                  
                  <Button
                      type="button"
                      on:click={toggleForm}
                      class="px-6 py-2.5 border bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all"
                  >
                      Cancel
                  </Button>
              </div>
          </form>
      </div>
  {/if}
</div>