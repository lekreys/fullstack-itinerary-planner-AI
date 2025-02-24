<script>
    import { onMount } from 'svelte';
    import ItineraryMap from './ItineraryMap.svelte';

    export let viewMode = "card"; 
    export let llm_result;

    const toggleView = (mode) => {
      viewMode = mode;
    };
</script>

<div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <h1 class="font-bold text-[2.5rem] text-black">Itinerary Result</h1>
      
      <div class="flex items-center bg-gray-100 p-1 rounded-lg">
        <button 
          class={`px-4 py-2 rounded-lg transition-all duration-200 ${viewMode === 'card' ? 'bg-white shadow text-orange-500' : 'text-gray-600 hover:text-gray-800'}`}
          on:click={() => toggleView('card')}
        >
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            Card View
          </div>
        </button>
        <button 
          class={`px-4 py-2 rounded-lg transition-all duration-200 ${viewMode === 'table' ? 'bg-white shadow text-orange-500' : 'text-gray-600 hover:text-gray-800'}`}
          on:click={() => toggleView('table')}
        >
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            Table View
          </div>
        </button>
      </div>
    </div>

    <div class="flex gap-4">
      <div class="w-6/12 h-[30rem] p-4 bg-white rounded-xl min-h-[200px] shadow-lg border">
        <div class="overflow-auto h-full">
          {#each llm_result.result as day}
            {#if viewMode === 'card'}
              <!-- Card View -->
              <div class="bg-white rounded-lg p-4 mb-4 shadow-lg">
                <div class="flex items-center justify-between mb-4">
                  <h2 class="text-xl font-bold text-gray-800">Day {day.day}</h2>
                  <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm">
                    {day.date}
                  </span>
                </div>
                
                <div class="space-y-4">
                  {#each day.schedule as data}
                    <div class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-all duration-300 cursor-pointer border border-gray-200">
                      <div class="flex justify-between items-start mb-2">
                        <span class="bg-orange-500 text-white px-2 py-1 rounded text-sm">
                          {data.time}
                        </span>
                        {#if data.ratings}
                          <div class="flex items-center bg-yellow-100 px-2 py-1 rounded">
                            <span class="text-yellow-500">★</span>
                            <span class="ml-1 text-sm">
                              {data.ratings}
                            </span>
                            <span class="text-xs text-gray-500 ml-1">
                              ({data.user_rating_total})
                            </span>
                          </div>
                        {/if}
                      </div>

                      <h3 class="font-semibold text-lg text-gray-800 mb-1">
                        {data.activity}
                      </h3>
                      
                      <div class="flex items-center text-gray-600 mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span class="text-sm">{data.location}</span>
                      </div>

                      {#if data.description}
                        <p class="text-sm text-gray-600 bg-gray-100 p-2 rounded">
                          {data.description}
                        </p>
                      {/if}

                      <div class="mt-2 text-xs text-gray-500">
                        <div class="flex flex-wrap gap-1">
                          {#each data.types as type}
                            <span class="bg-gray-200 px-2 py-1 rounded">
                              {type.replace('_', ' ')}
                            </span>
                          {/each}
                        </div>
                      </div>

                      <div class="mt-2 text-xs text-gray-500">
                        <span class="font-semibold">Location Code:</span> {data.global_code}
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {:else}
              <!-- Table View -->
              <div class="mb-6">
                <div class="flex items-center justify-between mb-4">
                  <h2 class="text-xl font-bold text-gray-800">Day {day.day}</h2>
                  <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm">
                    {day.date}
                  </span>
                </div>
                
                <div class="relative overflow-x-auto">
                  <table class="w-full text-sm text-left text-gray-500">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-100">
                      <tr>
                        <th scope="col" class="px-4 py-3">Time</th>
                        <th scope="col" class="px-4 py-3">Activity & Location</th>
                        <th scope="col" class="px-4 py-3">Details</th>
                        <th scope="col" class="px-4 py-3">Rating</th>
                      </tr>
                    </thead>
                    <tbody>
                      {#each day.schedule as data}
                        <tr class="bg-white border-b hover:bg-gray-50 cursor-pointer">
                          <td class="px-4 py-3">
                            <span class="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded">
                              {data.time}
                            </span>
                          </td>
                          <td class="px-4 py-3">
                            <div class="font-medium text-gray-900">
                              {data.activity}
                            </div>
                            <div class="text-xs text-gray-500 mt-1 flex items-center">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                              </svg>
                              {data.location}
                            </div>
                          </td>
                          <td class="px-4 py-3">
                            {#if data.description}
                              <div class="text-xs mb-2">
                                {data.description}
                              </div>
                            {/if}
                            <div class="flex flex-wrap gap-1">
                              {#each data.types as type}
                                <span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">
                                  {type.replace('_', ' ')}
                                </span>
                              {/each}
                            </div>
                            <div class="text-xs text-gray-400 mt-1">
                              Code: {data.global_code}
                            </div>
                          </td>
                          <td class="px-4 py-3">
                            {#if data.ratings}
                              <div class="flex items-center">
                                <span class="text-yellow-400 text-lg mr-1">★</span>
                                <div>
                                  <div class="font-medium">
                                    {data.ratings}
                                  </div>
                                  <div class="text-xs text-gray-400">
                                    {data.user_rating_total} reviews
                                  </div>
                                </div>
                              </div>
                            {:else}
                              <span class="text-gray-400">-</span>
                            {/if}
                          </td>
                        </tr>
                      {/each}
                    </tbody>
                  </table>
                </div>
              </div>
            {/if}
          {/each}
        </div>
      </div>

      <div class="flex-1 bg-white rounded-xl min-h-[200px] z-0 shadow-lg border">
        <ItineraryMap {llm_result} />
      </div>
    </div>
  </div>

<style>
  .overflow-auto::-webkit-scrollbar {
    width: 6px;
  }

  .overflow-auto::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }

  .overflow-auto::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
  }

  .overflow-auto::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

  thead {
    position: sticky;
    top: 0;
    z-index: 1;
    background: white;
  }
</style>