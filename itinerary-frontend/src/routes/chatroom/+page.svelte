<script>
    import Navbar from "$lib/component/navbar.svelte";
    import axios from "axios";
    import { fade } from 'svelte/transition';
    import { marked } from 'marked';
    import hljs from 'highlight.js';
    import 'highlight.js/styles/github-dark.css';
    import DOMPurify from 'dompurify';
    import { onMount } from 'svelte';

    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                return hljs.highlight(code, { language: lang }).value;
            }
            return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true
    });

    let history = [];
    let input = "";
    let isLoading = false;
    let chatContainer;
    let selectedModel = "gpt-3.5-turbo";
    let isSidebarOpen = true;

    const models = [
        { 
            id: "gpt-3.5-turbo", 
            name: "GPT-3.5 Turbo",
            description: "Fast and efficient for most tasks",
            icon: "🚀"
        },
        { 
            id: "gpt-4", 
            name: "GPT-4",
            description: "More powerful for complex tasks",
            icon: "⭐"
        },
        { 
            id: "gpt-4-turbo", 
            name: "GPT-4 Turbo",
            description: "Latest model with enhanced capabilities",
            icon: "✨"
        },
        { 
            id: "gpt-4o-mini", 
            name: "GPT-4o-mini",
            description: "mini model with enhanced capabilities",
            icon: "✨"
        }
    ];

    const templateQuestions = [
        {
            text: "Buatkan itinerary 3 hari di Bali untuk honeymoon",
            icon: "🌴"
        },
        {
            text: "Rekomendasi tempat kuliner tersembunyi di Jogja",
            icon: "🍜"
        },
        {
            text: "Tempat wisata terbaik di Bandung untuk keluarga",
            icon: "👨‍👩‍👧‍👦"
        },
        {
            text: "Tips traveling ke Jepang dengan budget 15 juta",
            icon: "✈️"
        },
        {
            text: "Rekomendasi penginapan romantis di Lombok",
            icon: "🏖️"
        },
        {
            text: "Rute road trip Jakarta ke Malang 3 hari",
            icon: "🚗"
        }
    ];

    function parseMarkdown(content) {
        const parsedContent = marked(content);
        return DOMPurify.sanitize(parsedContent);
    }

    $: if (history.length) {
        setTimeout(() => {
            chatContainer?.scrollTo(0, chatContainer.scrollHeight);
            // Reinitialize syntax highlighting
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }, 100);
    }

    async function to_llm() {
        if (!input.trim()) return;

        const send_input = {"role": "user", "content": input};
        history = [...history, send_input];
        const currentInput = input;
        input = ""; 
        isLoading = true;

        try {
            const response = await axios.post("http://localhost:8000/chatbot", {
                messages: history,
            });

            if (response.data) {
                history = [...history, response.data];
            }
        } catch (error) {
            console.error("Error:", error);
            input = currentInput;
            history = history.slice(0, -1);
            alert("Failed to send message. Please try again.");
        } finally {
            isLoading = false;
        }
    }

    function handleKeydown(event) {
        if (event.key === 'Enter' && !event.shiftKey && !isLoading) {
            event.preventDefault();
            to_llm();
        }
    }

    function clearChat() {
        history = [{
            "role": "system",
            "content": "You are a helpful assistant that provides clear and concise answers."
        }];
    }

    function useTemplate(question) {
        input = question;
    }

    onMount(() => {
        // Initialize highlight.js
        hljs.highlightAll();
    });
</script>

<Navbar />

<div class="min-h-[calc(100vh-30px)] mt-30 mx-auto max-w-7xl p-6 pt-28">
    <div class="flex gap-6 h-[calc(100vh-120px)]">
        <!-- Sidebar -->
        <div class="w-80 bg-white shadow-lg rounded-xl border border-gray-200 {isSidebarOpen ? '' : 'hidden'}">
            <div class="p-4">
                <h2 class="text-xl font-bold text-gray-800 mb-4">AI Models</h2>
                <div class="space-y-3">
                    {#each models as model}
                        <button
                            class="w-full p-4 rounded-xl text-left transition-all border {selectedModel === model.id ? 'bg-orange-100 border-orange-600' : 'border-gray-200 hover:border-orange-300'}"
                            on:click={() => selectedModel = model.id}
                        >
                            <div class="flex items-center gap-3">
                                <span class="text-2xl">{model.icon}</span>
                                <div>
                                    <div class="font-semibold text-gray-800">{model.name}</div>
                                    <div class="text-sm text-gray-600">{model.description}</div>
                                </div>
                            </div>
                        </button>
                    {/each}
                </div>

                <div class="mt-6">
                    <button
                        on:click={clearChat}
                        class="w-full p-3 rounded-lg border border-gray-200 hover:border-orange-300 hover:bg-orange-50 text-gray-700 font-medium transition-colors"
                    >
                        Clear Chat History
                    </button>
                </div>
            </div>
        </div>

        <!-- Main Chat Area -->
        <div class="flex-1 flex flex-col bg-white rounded-xl shadow-lg border border-gray-200">
            <!-- Toggle Sidebar Button -->
            <button
                class="absolute left-8 p-2 bg-orange-600 text-white rounded-lg shadow-md hover:bg-orange-700 transition-colors border border-orange-700 w-10 h-10 flex items-center justify-center"
                on:click={() => isSidebarOpen = !isSidebarOpen}
            >
                {isSidebarOpen ? '←' : '→'}
            </button>

            <!-- Template Questions -->
            {#if history.length === 1}
                <div class="p-6">
                    <h3 class="text-lg font-semibold text-gray-700 mb-4">Pilih pertanyaan tentang traveling:</h3>
                    <div class="grid grid-cols-2 gap-4">
                        {#each templateQuestions as question}
                            <button
                                class="p-4 rounded-xl border border-gray-200 hover:border-orange-300 hover:bg-orange-50 text-left transition-all group"
                                on:click={() => useTemplate(question.text)}
                            >
                                <div class="flex items-center gap-3">
                                    <span class="text-2xl group-hover:scale-110 transition-transform">{question.icon}</span>
                                    <span class="text-gray-700 text-sm md:text-base">{question.text}</span>
                                </div>
                            </button>
                        {/each}
                    </div>
                </div>
            {/if}

            <!-- Chat Container -->
            <div class="flex-1 p-6 overflow-hidden">
                <div 
                    bind:this={chatContainer}
                    class="h-full overflow-y-auto pr-4"
                >
                    {#each history as message}
                        {#if message.role !== 'system'}
                            <div 
                                transition:fade
                                class="mb-6 {message.role === 'user' ? 'flex justify-end' : 'flex justify-start'}"
                            >
                                <div class="{message.role === 'user' 
                                    ? 'bg-orange-600 text-white' 
                                    : 'bg-gray-100'} 
                                    p-4 rounded-2xl max-w-[80%] break-words shadow-md"
                                >
                                    {#if isLoading && message === history[history.length - 1]}
                                        <div class="flex items-center gap-2">
                                            <span>{message.content}</span>
                                            {#if message.role === 'user'}
                                                <span class="inline-block animate-spin">↻</span>
                                            {/if}
                                        </div>
                                    {:else}
                                        {#if message.role === 'user'}
                                            {message.content}
                                        {:else}
                                            <div class="markdown-content">
                                                {@html parseMarkdown(message.content)}
                                            </div>
                                        {/if}
                                    {/if}
                                </div>
                            </div>
                        {/if}
                    {/each}

                    {#if isLoading}
                        <div class="flex justify-start">
                            <div class="bg-gray-100 p-4 rounded-2xl">
                                <div class="flex gap-1">
                                    <span class="w-2 h-2 bg-orange-600 rounded-full animate-bounce"></span>
                                    <span class="w-2 h-2 bg-orange-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                                    <span class="w-2 h-2 bg-orange-600 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
                                </div>
                            </div>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Input Area -->
            <div class="p-4 border-t border-gray-200">
                <div class="flex gap-3">
                    <textarea
                        bind:value={input}
                        placeholder="Type your message..."
                        class="flex-1 p-4 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none h-[50px] max-h-[200px] overflow-y-auto text-lg"
                        on:keydown={handleKeydown}
                        disabled={isLoading}
                        rows="1"
                    />
                    <button
                        on:click={to_llm}
                        class="px-8 py-2 bg-orange-600 text-white rounded-xl hover:bg-orange-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md text-lg font-medium border border-orange-700"
                        disabled={!input.trim() || isLoading}
                    >
                        {#if isLoading}
                            <span class="inline-block animate-spin">↻</span>
                        {:else}
                            Send
                        {/if}
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    :global(*::-webkit-scrollbar) {
        width: 8px;
    }

    :global(*::-webkit-scrollbar-track) {
        background: #f1f1f1;
        border-radius: 10px;
    }

    :global(*::-webkit-scrollbar-thumb) {
        background: #ea580c;
        border-radius: 10px;
    }

    :global(*::-webkit-scrollbar-thumb:hover) {
        background: #c2410c;
    }

    /* Markdown Styles */
    :global(.markdown-content) {
        @apply text-gray-800 leading-relaxed;
    }

    :global(.markdown-content h1) {
        @apply text-2xl font-bold mb-4 mt-6 text-gray-900;
    }

    :global(.markdown-content h2) {
        @apply text-xl font-bold mb-3 mt-5 text-gray-900;
    }

    :global(.markdown-content h3) {
        @apply text-lg font-bold mb-2 mt-4 text-gray-900;
    }

    :global(.markdown-content p) {
        @apply mb-4 text-gray-700;
    }

    :global(.markdown-content ul) {
        @apply list-disc ml-6 mb-4 text-gray-700;
    }

    :global(.markdown-content ol) {
        @apply list-decimal ml-6 mb-4 text-gray-700;
    }

    :global(.markdown-content li) {
        @apply mb-2;
    }

    :global(.markdown-content a) {
        @apply text-orange-600 hover:text-orange-700 underline;
    }

    :global(.markdown-content blockquote) {
        @apply border-l-4 border-orange-500 pl-4 italic my-4 text-gray-600;
    }

    :global(.markdown-content pre) {
        @apply p-4 rounded-lg mb-4 overflow-x-auto bg-gray-900;
    }

    :global(.markdown-content code:not(pre code)) {
        @apply px-2 py-1 bg-gray-100 rounded text-sm font-mono text-orange-600;
    }

    :global(.markdown-content pre code) {
        @apply block text-sm font-mono;
    }

    :global(.markdown-content table) {
        @apply w-full border-collapse mb-4;
    }

    :global(.markdown-content th) {
        @apply bg-gray-100 border border-gray-300 px-4 py-2 text-left;
    }

    :global(.markdown-content td) {
        @apply border border-gray-300 px-4 py-2;
    }

    :global(.markdown-content img) {
        @apply max-w-full h-auto rounded-lg my-4;
    }

    :global(.markdown-content hr) {
        @apply my-8 border-gray-200;
    }

    :global(.markdown-content strong) {
        @apply font-bold text-gray-900;
    }

    :global(.markdown-content em) {
        @apply italic;
    }
</style>