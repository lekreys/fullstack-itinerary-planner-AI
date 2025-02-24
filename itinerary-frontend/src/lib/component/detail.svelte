<script>
    export let placeDetails = [];
    import { fade, slide, fly } from 'svelte/transition';
    import Button from '$lib/components/ui/button/button.svelte';

    let viewMode = 'list'; 
    let selectedPlace = null;
    let showModal = false;
    let searchQuery = '';

    // Filter places without names and apply search
    $: filteredPlaces = placeDetails
        .filter(place => place.name)
        .filter(place => 
            place.name.toLowerCase().includes(searchQuery.toLowerCase())
        );

    function formatTime(time) {
        if (!time) return '-';
        const hours = time.slice(0, 2);
        const minutes = time.slice(2);
        return `${hours}:${minutes}`;
    }

    const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    function formatOpeningHours(hours) {
        if (!hours) return 'No schedule available';
        return DAYS.map((day, index) => {
            const schedule = hours.find(h => h.open?.day === index);
            if (!schedule) return `${day}: Closed`;
            return `${day}: ${formatTime(schedule.open?.time)} - ${formatTime(schedule.close?.time)}`;
        });
    }

    function openModal(place) {
        selectedPlace = place;
        showModal = true;
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        showModal = false;
        selectedPlace = null;
        document.body.style.overflow = 'auto';
    }

    function toggleView() {
        viewMode = viewMode === 'list' ? 'table' : 'list';
    }
</script>

<!-- View Toggle and Search -->
<div class="max-w-full px-4 sm:px-6 lg:py-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <h1 class="text-[2.5rem] font-bold text-gray-900">Places Details</h1>
        <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <!-- Search Input -->
            <div class="relative w-full sm:w-64">
                <input
                    type="text"
                    bind:value={searchQuery}
                    placeholder="Search places..."
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-colors"
                />
                <svg 
                    class="absolute right-3 top-2.5 h-5 w-5 text-gray-400" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </div>
            <!-- View Toggle Button -->
            <Button 
                class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors w-full sm:w-auto"
                on:click={toggleView}
            >
                Switch to {viewMode === 'list' ? 'Table' : 'List'} View
            </Button>
        </div>
    </div>

    {#if viewMode === 'table'}
        <!-- Table View -->
        <div class="bg-white rounded-lg shadow">
            <div class="max-h-[600px] overflow-y-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50 sticky top-0 z-10">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rating</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reviews</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hours</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {#each filteredPlaces as place}
                            <tr class="hover:bg-gray-50 transition-colors">
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm font-medium text-gray-900">{place.name}</div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <span class="text-sm text-gray-900">{place.rating}</span>
                                        <span class="ml-1 text-yellow-400">★</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900">
                                        {place.location?.lat.toFixed(4)}, {place.location?.lng.toFixed(4)}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900">{place.reviews?.length || 0} reviews</div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <button 
                                        class="text-indigo-600 hover:text-indigo-900"
                                        on:click={() => openModal(place)}
                                    >
                                        View Details
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
    {:else}
        <!-- List View with Scrolling -->
        <div class="max-h-[600px] overflow-y-auto pr-2">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {#each filteredPlaces as place}
                    <div 
                        class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer"
                        on:click={() => openModal(place)}
                        in:fly="{{ y: 20, duration: 300 }}"
                    >
                        <div class="p-6">
                            <div class="flex justify-between items-start mb-4">
                                <h3 class="text-lg font-semibold text-gray-900">{place.name}</h3>
                                <div class="flex items-center bg-indigo-50 px-3 py-1 rounded-full">
                                    <span class="text-indigo-600 font-medium">{place.rating}</span>
                                    <span class="ml-1 text-yellow-400">★</span>
                                </div>
                            </div>
                            <div class="text-sm text-gray-500 space-y-2">
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    </svg>
                                    <span>{place.location?.lat.toFixed(4)}, {place.location?.lng.toFixed(4)}</span>
                                </div>
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                            d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                                    </svg>
                                    <span>{place.reviews?.length || 0} reviews</span>
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/if}

    <!-- Show "No results" message when search yields no results -->
    {#if filteredPlaces.length === 0}
        <div class="text-center py-10">
            <p class="text-gray-500 text-lg">No places found matching your search.</p>
        </div>
    {/if}
</div>

<!-- Modal Popup -->
{#if showModal && selectedPlace}
    <div class="fixed inset-0 z-50 overflow-y-auto"
         transition:fade
         on:click={closeModal}>
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75" transition:fade={{ duration: 200 }}></div>

            <!-- Modal panel -->
            <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full"
                 on:click|stopPropagation
                 transition:fly="{{ y: 100, duration: 300 }}">
                
                <!-- Header with background image -->
                <div class="relative h-48 bg-gradient-to-r from-orange-400 to-orange-600 flex items-end">
                    <div class="absolute inset-0 bg-black opacity-20"></div>
                    <div class="relative p-6 text-white">
                        <h2 class="text-3xl font-bold mb-2">{selectedPlace.name}</h2>
                        <div class="flex items-center space-x-4">
                            <div class="flex items-center">
                                <span class="text-xl font-bold">{selectedPlace.rating}</span>
                                <span class="ml-1 text-yellow-300 text-xl">★</span>
                            </div>
                            <span class="text-white/80">|</span>
                            <span>{selectedPlace.reviews?.length || 0} reviews</span>
                        </div>
                    </div>
                    <button 
                        class="absolute top-4 right-4 text-white/80 hover:text-white transition-colors"
                        on:click={closeModal}
                    >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <!-- Content -->
                <div class="bg-gray-50">
                    <div class="grid grid-cols-3 divide-x divide-gray-200">
                        <!-- Quick Info -->
                        <div class="p-6">
                            <h3 class="text-lg font-semibold text-gray-900 mb-4">Location</h3>
                            <div class="space-y-3">
                                <div class="text-sm text-gray-600">
                                    <div class="font-medium text-gray-900 mb-1">Coordinates</div>
                                    <div>Lat: {selectedPlace.location?.lat.toFixed(6)}</div>
                                    <div>Lng: {selectedPlace.location?.lng.toFixed(6)}</div>
                                </div>
                            </div>
                        </div>

                        <!-- Hours -->
                        <div class="p-6">
                            <h3 class="text-lg font-semibold text-gray-900 mb-4">Opening Hours</h3>
                            <div class="space-y-2">
                                {#if selectedPlace.opening_hours}
                                    {#each formatOpeningHours(selectedPlace.opening_hours) as schedule}
                                        <div class="text-sm text-gray-600">{schedule}</div>
                                    {/each}
                                {:else}
                                    <p class="text-sm text-gray-500">Hours not available</p>
                                {/if}
                            </div>
                        </div>

                        <!-- Reviews Preview -->
                        <div class="p-6">
                            <h3 class="text-lg font-semibold text-gray-900 mb-4">Latest Reviews</h3>
                            <div class="space-y-4">
                                {#if selectedPlace.reviews && selectedPlace.reviews.length > 0}
                                    {#each selectedPlace.reviews.slice(0, 2) as review}
                                        <div class="text-sm">
                                            <div class="flex items-center justify-between mb-1">
                                                <span class="font-medium text-gray-900">{review.author_name}</span>
                                                <div class="flex items-center">
                                                    <span class="text-gray-900">{review.rating}</span>
                                                    <span class="ml-1 text-yellow-400">★</span>
                                                </div>
                                            </div>
                                            <p class="text-gray-600 line-clamp-2">{review.text}</p>
                                        </div>
                                    {/each}
                                {:else}
                                    <p class="text-sm text-gray-500">No reviews yet</p>
                                {/if}
                            </div>
                        </div>
                    </div>

                    <!-- Full Reviews Section -->
                    <div class="border-t border-gray-200">
                        <div class="p-6">
                            <h3 class="text-lg font-semibold text-gray-900 mb-4">All Reviews</h3>
                            <div class="space-y-4 max-h-[300px] overflow-y-auto pr-2">
                                {#if selectedPlace.reviews && selectedPlace.reviews.length > 0}
                                    {#each selectedPlace.reviews as review}
                                        <div class="bg-white rounded-lg p-4 shadow-sm">
                                            <div class="flex items-center justify-between mb-2">
                                                <div class="flex items-center">
                                                    <img 
                                                        src={review.profile_photo_url} 
                                                        alt={review.author_name}
                                                        class="w-10 h-10 rounded-full border-2 border-indigo-200"
                                                    />
                                                    <div class="ml-3">
                                                        <p class="font-medium text-gray-900">{review.author_name}</p>
                                                        <p class="text-xs text-gray-500">{review.relative_time_description}</p>
                                                    </div>
                                                </div>
                                                <div class="bg-gray-50 px-3 py-1 rounded-full">
                                                    <span class="text-indigo-600 font-medium">{review.rating}</span>
                                                    <span class="text-yellow-400">★</span>
                                                </div>
                                            </div>
                                            <p class="text-gray-600 text-sm">{review.text}</p>
                                        </div>
                                    {/each}
                                {:else}
                                    <p class="text-center text-gray-500">No reviews available</p>
                                {/if}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .overflow-y-auto {
        scrollbar-width: thin;
        scrollbar-color: #f2911b #EEF2FF;
    }

    .overflow-y-auto::-webkit-scrollbar {
        width: 6px;
    }

    .overflow-y-auto::-webkit-scrollbar-track {
        background: #EEF2FF;
        border-radius: 3px;
    }

    .overflow-y-auto::-webkit-scrollbar-thumb {
        background-color: #fba535;
        border-radius: 3px;
    }

    thead {
        position: sticky;
        top: 0;
        background-color: #F9FAFB;
        z-index: 10;
    }
</style>