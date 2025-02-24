<script lang="ts">
    import { Button } from "$lib/components/ui/button";
</script>

<nav class="bg-orange-200 h-20 w-full fixed z-50">
    <div class="flex items-center h-full px-14">
        <div class="absolute left-14">
            <svg 
                width="40" 
                height="40" 
                viewBox="0 0 64.00 64.00" 
                xmlns="http://www.w3.org/2000/svg" 
                class="cursor-pointer hover:scale-110 transition-transform"
            >
                <g id="SVGRepo_iconCarrier">
                    <title>beach</title>
                    <g id="beach">
                        <circle cx="37.5" cy="22.5" r="21.5" style="fill:#e5efef"></circle>
                        <path d="M29.861,10.947a12.316,12.316,0,1,1-3.694-3.868" style="fill:#ffce56;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></path>
                        <path d="M21.327,15.913a16.929,16.929,0,0,0-2.434,4.67s4.095-.8,4.924,2.515c0,0,4.976-2.488,7.464,1.659,0,0,6.634-2.488,9.122,2.488,0,0,3.317-3.318,7.463.829,0,0,.554-1.1,2.951-.892a1.132,1.132,0,0,0,1.2-1.148A17,17,0,0,0,35.012,9h-.056a16.179,16.179,0,0,0-7.329,1.907l-.652.336A16.155,16.155,0,0,0,21.327,15.913Z" style="fill:#ffffff;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></path>
                        <path d="M38.752,9.418a16.935,16.935,0,0,0-1.786-.3A21.285,21.285,0,0,0,23.817,23.1s4.976-2.488,7.463,1.659A22.036,22.036,0,0,1,38.752,9.418Z" style="fill:#fc8c29;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></path>
                        <path d="M62.455,39a5.069,5.069,0,0,0-4.859.433h0a6.136,6.136,0,0,1-5.782,0h0a6.151,6.151,0,0,0-5.4-.187l-1.372.619a6.156,6.156,0,0,1-5.026,0l-1.371-.619a6.151,6.151,0,0,0-5.4.187h0a6.136,6.136,0,0,1-5.782,0h0a6.151,6.151,0,0,0-5.4-.187l-1.371.619a6.156,6.156,0,0,1-5.026,0l-1.372-.619a6.151,6.151,0,0,0-5.4.187h0a6.136,6.136,0,0,1-5.782,0h0a6.034,6.034,0,0,0-2.224-.687V52H62.455Z" style="fill:#9dc1e4"></path>
                        <path d="M43.106,11.047a16.856,16.856,0,0,0-2.126-.967c.971,3.6,2.539,11.555-.577,17.164,0,0,3.317-3.317,7.464.83A21.331,21.331,0,0,0,43.106,11.047Z" style="fill:#fc8c29;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></path>
                        <line x1="28.366" y1="52.639" x2="36" y2="25" style="fill:none;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></line>
                        <path d="M11.8,55H1a8,8,0,0,1,8-8H55a8,8,0,0,1,8,8H19.409" style="fill:#ffe8dc;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></path>
                        <path d="M63,39.246a6.151,6.151,0,0,0-5.4.187h0a6.136,6.136,0,0,1-5.782,0h0a6.151,6.151,0,0,0-5.4-.187l-1.372.619a6.156,6.156,0,0,1-5.026,0l-1.371-.619a6.151,6.151,0,0,0-5.4.187h0a6.136,6.136,0,0,1-5.782,0h0a6.151,6.151,0,0,0-5.4-.187l-1.371.619a6.156,6.156,0,0,1-5.026,0l-1.372-.619a6.151,6.151,0,0,0-5.4.187h0a6.136,6.136,0,0,1-5.782,0h0a6.034,6.034,0,0,0-2.224-.687" style="fill:none;stroke:#4c241d;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px"></path>
                    </g>
                </g>
            </svg>
        </div>

        <ul class="flex gap-10 text-lg font-medium mx-auto">
            <li class="cursor-pointer hover:text-orange-600 hover:underline transition-all">
                <a href="/">Home</a>
            </li>
            <li class="cursor-pointer hover:text-orange-600 hover:underline transition-all">
                <a href="/chatroom">Trip Consultation</a>
            </li>
            <li class="cursor-pointer hover:text-orange-600 hover:underline transition-all">
                <a href="/itinerary">Plan Your Trip</a>
            </li>
            <li class="cursor-pointer hover:text-orange-600 hover:underline transition-all">
                <a href="/about">About Us</a>
            </li>
            
        </ul>

        <Button 
            class="absolute right-14 bg-orange-500 hover:bg-orange-600 text-white  text-md"
            size="lg"
        >
            Login
        </Button>
    </div>
</nav>
