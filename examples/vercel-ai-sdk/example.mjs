import { generateText } from 'ai';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';

const mockllm = createOpenAICompatible({
  name: 'mockllm',
  apiKey: 'mock-key',
  baseURL: 'http://localhost:8000/v1',
});

const { text } = await generateText({
  model: mockllm('gpt-4o'),
  prompt: 'hello',
});

console.log('\n=== Vercel AI SDK Response ===\n');
console.log(text);
