<!-- src/routes/about/+page.svelte -->
<script>
    import { Button } from "$lib/components/ui/button";
    import Navbar from "$lib/component/navbar.svelte";
  
    const profile = {
      name: "Lekrey Jerel Jacob Laipiopa",
      role: "AI Developer Intern",
      email: "lekrey.laipiopa29@gmail.com",
      location: "Jakarta, Indonesia",
      bio: "AI Developer passionate about building innovative solutions combining artificial intelligence and web technologies. Currently focusing on developing intelligent travel planning systems and AI-powered applications.",
      experience: "AI Development Intern",
      github: "https://github.com/lekreys",
      linkedin: "https://www.linkedin.com/in/lekrey/"
    };
  
    const technologies = [
      {
        category: "AI & Machine Learning",
        items: [
          { name: "Google Gemini", icon: "🤖", description: "Large Language Model for intelligent conversation and content generation" },
          { name: "ChatGPT", icon: "🧠", description: "AI model integration for natural language processing" },
          { name: "LangChain", icon: "⛓️", description: "Framework for developing applications powered by language models" }
        ]
      },
      {
        category: "Frontend Development",
        items: [
          { name: "SvelteKit", icon: "🔥", description: "Modern web framework for building fast, efficient applications" },
          { name: "Tailwind CSS", icon: "🎨", description: "Utility-first CSS framework for rapid UI development" }
        ]
      },
      {
        category: "Backend & API",
        items: [
          { name: "FastAPI", icon: "⚡", description: "Modern Python framework for building high-performance APIs" }
        ]
      },
      {
        category: "Maps & Geospatial",
        items: [
          { name: "Google Maps API", icon: "🗺️", description: "Location services and mapping functionality" },
          { name: "Leaflet", icon: "📍", description: "Open-source library for interactive maps" }
        ]
      }
    ];
  </script>

    <Navbar />
  
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white py-32 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto">
      <!-- Hero Section -->
      <div class="flex flex-col md:flex-row items-center gap-12 mb-16">
        <!-- Profile Image -->
        <div class="w-full md:w-1/3">
          <div class="relative">
            <img
              src="/portt.jpg" 
              alt={profile.name}
              class="rounded-2xl shadow-xl w-full object-cover aspect-square hover:scale-105 transition-transform duration-300"
            />
            <div class="absolute -bottom-4 -right-4 bg-primary text-white px-6 py-2 rounded-lg shadow-lg">
              {profile.role}
            </div>
          </div>
        </div>
  
        <!-- Introduction -->
        <div class="w-full md:w-2/3 space-y-6">
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900">
            Hi, I'm <span class="text-primary">{profile.name}</span> 👋
          </h1>
          <p class="text-xl text-gray-600 leading-relaxed">
            {profile.bio}
          </p>
          
          <!-- Quick Info -->
          <div class="flex flex-wrap gap-4 text-gray-600">
            <span class="flex items-center gap-2">
              📍 {profile.location}
            </span>
            <span class="flex items-center gap-2">
              💼 {profile.experience}
            </span>
          </div>
  
          <!-- Contact Buttons -->
          <div class="flex flex-wrap gap-4 pt-4">

            <a href="mailto:{profile.email}">
  
                <Button variant="default" class="flex items-center gap-2">
                📧 Contact Me
                </Button>
            </a>

            <a href={profile.github}>

                <Button variant="outline" class="flex items-center gap-2">
                💻 GitHub
                </Button>
        
            </a>

            <a href={profile.linkedin}>
                <Button variant="outline" class="flex items-center gap-2">
                    💼 LinkedIn
      
                  </Button>
            </a>

          </div>
        </div>
      </div>
  
      <!-- Technology Stack -->
      <div class="mb-20">
        <h2 class="text-3xl font-bold text-center mb-12">Technology Stack</h2>
        
        {#each technologies as category}
          <div class="mb-12">
            <h3 class="text-2xl font-semibold mb-6">{category.category}</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {#each category.items as tech}
                <div class="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all hover:-translate-y-1">
                  <div class="flex items-start gap-4">
                    <span class="text-3xl">{tech.icon}</span>
                    <div>
                      <h4 class="text-xl font-semibold mb-2">{tech.name}</h4>
                      <p class="text-gray-600">{tech.description}</p>
                    </div>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>
  
      <!-- Current Project -->
      <div class="bg-white rounded-2xl p-8 shadow-lg mb-20">
        <h2 class="text-3xl font-bold mb-6">Current Project: AI-Powered Travel Itinerary Generator</h2>
        <div class="space-y-6">
          <p class="text-gray-600">
            Developing an intelligent travel planning system that combines AI and mapping technologies to create 
            personalized travel itineraries. The system leverages:
          </p>
          <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <li class="flex items-center gap-2 text-gray-600">
              ✨ AI-powered recommendations using Gemini & ChatGPT
            </li>
            <li class="flex items-center gap-2 text-gray-600">
              🔄 LangChain for complex AI workflow management
            </li>
            <li class="flex items-center gap-2 text-gray-600">
              🗺️ Interactive mapping with Google Maps & Leaflet
            </li>
            <li class="flex items-center gap-2 text-gray-600">
              ⚡ High-performance backend with FastAPI
            </li>
          </ul>
        </div>
      </div>
  
     
      </div>
  
      <!-- Contact Section -->
      <div class="bg-gray-50 rounded-2xl p-8 shadow-inner">
        <h2 class="text-3xl font-bold text-center mb-8">Let's Connect!</h2>
        <div class="max-w-2xl mx-auto space-y-6 text-center">
          <p class="flex items-center justify-center gap-2 text-lg">
            📧 <a href={`mailto:${profile.email}`} class="text-primary hover:underline">
              {profile.email}
            </a>
          </p>
          <p class="text-gray-600">
            Interested in AI development or have a project in mind? Let's discuss how we can work together!
          </p>
        </div>
      </div>
    </div>
