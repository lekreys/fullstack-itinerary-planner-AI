<script>
  import Navbar from "$lib/component/navbar.svelte";
  import Form from "$lib/component/form.svelte";
  import { fade, slide, fly } from 'svelte/transition';
  import Result from "$lib/component/result.svelte";
  import Detail from "$lib/component/detail.svelte";

  let inputpromptdata = null;
  let llm_result = null;
  let isGenerating = false;
  let place_ids_list = null;
  let isSidebarOpen = true;

  const handlePlaceUpdate = (event) => {
    const { place, llm_result: newLlmResult, ids } = event.detail;
    inputpromptdata = place;
    llm_result = newLlmResult;
    isGenerating = false;
    place_ids_list = ids;
  };

  const toggleSidebar = () => {
    isSidebarOpen = !isSidebarOpen;
  };

  const openSidebar = () => {
    isSidebarOpen = true;
  };

  const features = [
    { icon: "🎯", title: "Smart Planning", description: "AI-powered itinerary creation" },
    { icon: "🗺️", title: "Local Insights", description: "Discover hidden gems" },
    { icon: "⭐", title: "Top Attractions", description: "Must-visit locations" },
    { icon: "📅", title: "Day-by-Day", description: "Organized schedule" },
  ];
</script>

<Navbar />

<main class="pt-20 p-10">
  <div class="flex bg-white mt-7 rounded-xl min-h-[600px] shadow-lg border relative">
    <!-- Sidebar Toggle Button -->
    {#if llm_result}
      <button
        class="absolute -left-3 top-1/2 transform -translate-y-1/2 bg-orange-500 text-white rounded-full p-2 shadow-lg z-10 hover:bg-orange-600 transition-colors duration-300"
        on:click={toggleSidebar}
      >
        <svg
          class="w-4 h-4 transform {isSidebarOpen ? 'rotate-0' : 'rotate-180'}"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
      </button>
    {/if}

    <!-- Sidebar Section -->
    <div
      class="border-r border-orange-100 flex flex-col transition-all duration-300 ease-in-out overflow-hidden "
      class:w-[600px]={isSidebarOpen}
      class:w-0={!isSidebarOpen}
    >
      {#if isSidebarOpen}
        <div class="p-6 border-b border-orange-100">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Plan Your Journey</h2>
          <p class="text-gray-600">Create your perfect travel itinerary in minutes</p>
        </div>

        <div class="p-6 overflow-y-auto h-full">
          <!-- Form always visible -->
          <Form on:placeUpdate={handlePlaceUpdate} />
          
          <!-- Quick Actions -->
          {#if llm_result}
            <div class="space-y-3 mt-6">
              <button class="w-full px-4 py-2 bg-orange-100 hover:bg-orange-200 rounded-lg text-left flex items-center gap-2 transition-colors">
                <span>📋</span> View Full Itinerary
              </button>
              <button class="w-full px-4 py-2 bg-orange-100 hover:bg-orange-200 rounded-lg text-left flex items-center gap-2 transition-colors">
                <span>🗺️</span> Show on Map
              </button>
              <button class="w-full px-4 py-2 bg-orange-100 hover:bg-orange-200 rounded-lg text-left flex items-center gap-2 transition-colors">
                <span>💾</span> Save Itinerary
              </button>
            </div>
          {/if}

          <!-- Tips Section -->
          <div class="mt-8 bg-orange-50 rounded-lg p-4">
            <h3 class="font-semibold text-gray-800 flex items-center gap-2">
              <span>💡</span> Travel Tips
            </h3>
            <ul class="mt-2 space-y-2 text-sm text-gray-600">
              <li class="flex items-center gap-2">
                <span class="w-1 h-1 bg-orange-400 rounded-full"></span>
                Choose the duration that best fits your schedule
              </li>
              <li class="flex items-center gap-2">
                <span class="w-1 h-1 bg-orange-400 rounded-full"></span>
                Be specific with your destination for better results
              </li>
              <li class="flex items-center gap-2">
                <span class="w-1 h-1 bg-orange-400 rounded-full"></span>
                Review generated itineraries and customize as needed
              </li>
            </ul>
          </div>
        </div>
      {/if}
    </div>

    <!-- Main Content Section -->
    <div class="flex-1 p-8">
      {#if !inputpromptdata}
        <!-- Empty State -->
        <div 
          class="h-full flex flex-col items-center justify-center text-center space-y-4"
          transition:fade
        >
          <div class="text-6xl">🌍</div>
          <h2 class="text-2xl font-semibold text-gray-700">Ready to Start Planning?</h2>
          <p class="text-gray-500 max-w-md">
            Fill in your travel details to generate a personalized itinerary
          </p>
          <div class="mt-4 grid grid-cols-2 gap-4 max-w-md">
            <div class="p-4 bg-orange-50 rounded-lg text-center">
              <span class="block text-2xl mb-2">📍</span>
              <span class="text-sm text-gray-600">Choose Location</span>
            </div>
            <div class="p-4 bg-orange-50 rounded-lg text-center">
              <span class="block text-2xl mb-2">📅</span>
              <span class="text-sm text-gray-600">Set Duration</span>
            </div>
          </div>
        </div>
      {:else}
        <!-- Generated Content -->
        <div class="flex flex-col" in:fly="{{ y: 20, duration: 500 }}">
          <div class="flex justify-between items-center">
            <h1 class="font-bold text-2xl text-gray-800 flex items-center flex-wrap gap-2">
              <span class="inline-flex items-center">
                Itinerary to:
              </span>
              
              <div 
                class="relative group"
                transition:slide
              >
                <span class="text-4xl text-orange-500 inline-block truncate max-w-[500px] hover:max-w-full transition-all duration-300 ease-in-out">
                  {inputpromptdata.location}
                </span>
                
                {#if inputpromptdata.location.length > 30}
                  <div class="absolute left-0 -bottom-8 hidden group-hover:block bg-gray-800 text-white text-sm rounded px-2 py-1 whitespace-nowrap z-10">
                    {inputpromptdata.location}
                  </div>
                {/if}
              </div>
            </h1>

            <!-- Edit Button -->
            <button
              class="flex items-center gap-2 px-4 py-2 bg-orange-100 hover:bg-orange-200 rounded-lg transition-colors text-gray-700"
              on:click={openSidebar}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
              Edit Journey
            </button>
          </div>

          <div 
            class="mt-8 space-y-4"
            transition:fade
          >
            <div class="bg-orange-50 rounded-lg p-4 border border-orange-200 hover:bg-orange-100/50 transition-all duration-300">
              <h3 class="text-gray-800 font-semibold mb-2">Itinerary Overview</h3>
              <p class="text-gray-600">
                {#if isGenerating}
                  Crafting your perfect {inputpromptdata.days}-day journey to {inputpromptdata.location}...
                {:else}
                  Planning a {inputpromptdata.days}-day adventure in {inputpromptdata.location}
                {/if}
              </p>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="bg-orange-50 rounded-lg p-4 border border-orange-200 hover:bg-orange-100/50 transition-all duration-300 group">
                <h3 class="text-gray-800 font-semibold mb-2 group-hover:text-orange-600">
                  <span class="inline-block mr-2">📍</span>Maps
                </h3>
                <p class="text-gray-600">Interactive destination maps</p>
              </div>
              
              <div class="bg-orange-50 rounded-lg p-4 border border-orange-200 hover:bg-orange-100/50 transition-all duration-300 group">
                <h3 class="text-gray-800 font-semibold mb-2 group-hover:text-orange-600">
                  <span class="inline-block mr-2">✨</span>Recommendations
                </h3>
                <p class="text-gray-600">AI-powered place suggestions</p>
              </div>
            </div>
          </div>

          <!-- Status Cards -->
          <div class="mt-4 grid grid-cols-3 gap-4">
            <div class="bg-white rounded-lg p-4 border border-orange-200 shadow-sm hover:shadow-md transition-all duration-300">
              <div class="text-orange-500 mb-2">🗓️</div>
              <h4 class="font-medium text-gray-800">Duration</h4>
              <p class="text-gray-600">{inputpromptdata.days} Days</p>
            </div>

            <div class="bg-white rounded-lg p-4 border border-orange-200 shadow-sm hover:shadow-md transition-all duration-300">
              <div class="text-orange-500 mb-2">📍</div>
              <h4 class="font-medium text-gray-800">Destination</h4>
              <p class="text-gray-600 truncate" title={inputpromptdata.location}>{inputpromptdata.location}</p>
            </div>

            <div class="bg-white rounded-lg p-4 border border-orange-200 shadow-sm hover:shadow-md transition-all duration-300">
              <div class="text-orange-500 mb-2">✨</div>
              <h4 class="font-medium text-gray-800">Status</h4>
              <p class="text-gray-600">
                {#if isGenerating}
                  <span class="inline-flex items-center">
                    <svg class="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                    </svg>
                    Generating...
                  </span>
                {:else if llm_result}
                  Generated
                {:else}
                  Waiting to generate
                {/if}
              </p>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Results Section -->
  {#if inputpromptdata && llm_result}
    <div in:fade="{{ duration: 300, delay: 200 }}">
      <Result llm_result={llm_result} />
      <Detail placeDetails={place_ids_list} />
    </div>
  {/if}
</main>

<style>
  .truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>