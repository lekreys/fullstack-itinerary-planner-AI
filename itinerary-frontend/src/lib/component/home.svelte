<script>
    import Button from "$lib/components/ui/button/button.svelte";
    
    const features = [
        {
            title: "AI-Powered Planning",
            description: "Advanced AI algorithms create personalized travel itineraries based on your preferences",
            icon: "🤖"
        },
        {
            title: "Interactive Maps",
            description: "Visualize your entire journey with interactive maps and route planning",
            icon: "🗺️"
        },
        {
            title: "Smart Recommendations",
            description: "Get intelligent suggestions for attractions, restaurants, and activities",
            icon: "⭐"
        }
    ];
</script>

<div class="container mx-auto px-8 font-montserrat">
    <!-- Hero Section -->
    <div class="flex gap-12 items-center mb-32">
        <!-- Bagian Kiri -->
        <div class="w-8/12 pr-8">
            <div class="inline-block px-4 py-2 bg-orange-100 rounded-full mb-4">
                <span class="text-orange-600 font-semibold">✨ AI-Powered Travel Planning</span>
            </div>
            
            <h1 class="text-[8rem] leading-none font-bold mb-6">
                Wanderly
            </h1>
            
            <p class="text-2xl font-semibold text-gray-800 mb-6 leading-relaxed">
                Travia – Smart AI-Powered Itinerary Planning for Seamless, Effortless, and Unforgettable Journeys
            </p>
            
            <p class="text-xl text-gray-600 leading-relaxed mb-10">
                Travia is an AI-powered platform that simplifies automatic travel planning. With support from multiple LLM models, Travia can generate itineraries based on destinations, duration, and user preferences. Additionally, users can explore popular destinations for inspiration before creating their travel plans. Every generated itinerary is displayed interactively on a map, allowing users to visualize their routes more clearly. With Travia, travel planning becomes faster, smarter, and more convenient!
            </p>

            <Button 
                class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-6 text-lg font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
            >
                <a href="/itinerary">Make Itinerary</a>
            </Button>
        </div>

        <!-- Bagian Kanan -->
        <div class="w-4/12">
            <div class="relative p-12">
                <img 
                    src="home.jpg" 
                    alt="Travel Planning" 
                    class="rounded-2xl w-full h-auto object-cover shadow-[0_20px_50px_rgba(8,_112,_184,_0.7)] hover:shadow-[0_20px_50px_rgba(8,_112,_184,_0.4)] transition-all duration-300"
                />
                
                <div class="absolute -z-10 top-4 right-4 w-9/12 h-[36rem] bg-orange-200 rounded-2xl"></div>
            </div>
        </div>
    </div>

    <!-- Features Section -->
    <section class="py-20 bg-orange-50 rounded-3xl mb-32">
        <div class="text-center mb-16">
            <h2 class="text-4xl font-bold mb-6">Why Choose Wanderly?</h2>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Experience the perfect blend of AI technology and travel expertise
            </p>
        </div>
        
        <div class="grid grid-cols-3 gap-8 px-12">
            {#each features as feature}
                <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300">
                    <div class="text-4xl mb-4">{feature.icon}</div>
                    <h3 class="text-xl font-bold mb-3">{feature.title}</h3>
                    <p class="text-gray-600">{feature.description}</p>
                </div>
            {/each}
        </div>
    </section>

    <!-- How It Works Section -->
    <section class="mb-32">
        <div class="text-center mb-16">
            <h2 class="text-4xl font-bold mb-6">How It Works</h2>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Three simple steps to your perfect travel itinerary
            </p>
        </div>

        <div class="flex justify-between gap-12">
            <div class="flex-1 text-center">
                <div class="text-5xl mb-4">1️⃣</div>
                <h3 class="text-xl font-bold mb-2">Choose Destination</h3>
                <p class="text-gray-600">Select your dream destination and travel dates</p>
            </div>
            <div class="flex-1 text-center">
                <div class="text-5xl mb-4">2️⃣</div>
                <h3 class="text-xl font-bold mb-2">Set Preferences</h3>
                <p class="text-gray-600">Tell us about your interests and travel style</p>
            </div>
            <div class="flex-1 text-center">
                <div class="text-5xl mb-4">3️⃣</div>
                <h3 class="text-xl font-bold mb-2">Get Itinerary</h3>
                <p class="text-gray-600">Receive your AI-generated perfect itinerary</p>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-orange-50 rounded-3xl py-20 px-8 mb-32 text-center">
        <h2 class="text-4xl font-bold mb-6">Ready to Plan Your Next Adventure?</h2>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Let our AI help you create the perfect travel itinerary in minutes
        </p>
        <Button 
            class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-6 text-lg font-semibold rounded-lg transition-all duration-300 hover:shadow-lg"
        >
            <a href="/itinerary">Start Planning Now</a>
        </Button>
    </section>
</div>

<style>
    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    @keyframes marquee-reverse {
        0% { transform: translateX(-50%); }
        100% { transform: translateX(0); }
    }

    .animate-marquee {
        animation: marquee 30s linear infinite;
    }
</style>