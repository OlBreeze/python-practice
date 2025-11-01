# Интеграция AI моделей в Java-сервисы

## 1. **Через API (самый распространенный способ)**

### OpenAI API
```java
@Service
public class OpenAIService {
    private final RestTemplate restTemplate;
    private final String apiKey;
    
    public String generateText(String prompt) {
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(apiKey);
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        Map<String, Object> request = Map.of(
            "model", "gpt-4",
            "messages", List.of(
                Map.of("role", "user", "content", prompt)
            ),
            "temperature", 0.7
        );
        
        HttpEntity<Map<String, Object>> entity = 
            new HttpEntity<>(request, headers);
            
        ResponseEntity<OpenAIResponse> response = 
            restTemplate.postForEntity(
                "https://api.openai.com/v1/chat/completions",
                entity,
                OpenAIResponse.class
            );
            
        return response.getBody().getChoices().get(0)
            .getMessage().getContent();
    }
}
```

### Azure OpenAI
```java
@Service
public class AzureOpenAIService {
    @Value("${azure.openai.endpoint}")
    private String endpoint;
    
    @Value("${azure.openai.api-key}")
    private String apiKey;
    
    public String chat(String userMessage) {
        OpenAIClient client = new OpenAIClientBuilder()
            .credential(new AzureKeyCredential(apiKey))
            .endpoint(endpoint)
            .buildClient();
            
        List<ChatMessage> chatMessages = new ArrayList<>();
        chatMessages.add(new ChatMessage(ChatRole.USER)
            .setContent(userMessage));
            
        ChatCompletions completions = client.getChatCompletions(
            "gpt-4-deployment-name",
            new ChatCompletionsOptions(chatMessages)
        );
        
        return completions.getChoices().get(0)
            .getMessage().getContent();
    }
}
```

## 2. **Через HuggingFace API**

```java
@Service
public class HuggingFaceService {
    private final WebClient webClient;
    
    public HuggingFaceService(WebClient.Builder builder) {
        this.webClient = builder
            .baseUrl("https://api-inference.huggingface.co/models")
            .defaultHeader("Authorization", "Bearer " + apiKey)
            .build();
    }
    
    public Mono<String> classify(String text) {
        Map<String, String> request = Map.of("inputs", text);
        
        return webClient.post()
            .uri("/distilbert-base-uncased-finetuned-sst-2-english")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(String.class);
    }
}
```

## 3. **Локальный запуск моделей (через Python микросервис)**

### Python FastAPI сервис
```python
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()
classifier = pipeline("sentiment-analysis")

@app.post("/analyze")
async def analyze_sentiment(text: str):
    result = classifier(text)
    return {"sentiment": result[0]["label"], 
            "confidence": result[0]["score"]}
```

### Java клиент
```java
@Service
public class MLMicroserviceClient {
    private final RestTemplate restTemplate;
    
    public SentimentResult analyzeSentiment(String text) {
        String url = "http://ml-service:8000/analyze";
        
        Map<String, String> request = Map.of("text", text);
        
        return restTemplate.postForObject(
            url, 
            request, 
            SentimentResult.class
        );
    }
}
```

## 4. **Embedding и векторный поиск**

```java
@Service
public class EmbeddingService {
    private final OpenAIClient openAIClient;
    
    public float[] getEmbedding(String text) {
        EmbeddingsOptions options = new EmbeddingsOptions(
            List.of(text)
        );
        
        Embeddings embeddings = openAIClient.getEmbeddings(
            "text-embedding-ada-002",
            options
        );
        
        return embeddings.getData().get(0)
            .getEmbeddingAsFloatArray();
    }
}

@Service
public class VectorSearchService {
    private final PineconeClient pinecone; // или Weaviate, Milvus
    
    public List<Document> semanticSearch(String query) {
        float[] queryEmbedding = embeddingService
            .getEmbedding(query);
            
        QueryResponse response = pinecone.query(
            QueryRequest.newBuilder()
                .setVector(queryEmbedding)
                .setTopK(5)
                .build()
        );
        
        return response.getMatchesList().stream()
            .map(this::toDocument)
            .collect(Collectors.toList());
    }
}
```

## 5. **RAG (Retrieval-Augmented Generation)**

```java
@Service
public class RAGService {
    private final VectorSearchService vectorSearch;
    private final OpenAIService openAI;
    
    public String answerQuestion(String question) {
        // 1. Найти релевантные документы
        List<Document> relevantDocs = vectorSearch
            .semanticSearch(question);
        
        // 2. Составить контекст
        String context = relevantDocs.stream()
            .map(Document::getContent)
            .collect(Collectors.joining("\n\n"));
        
        // 3. Отправить в LLM с контекстом
        String prompt = String.format(
            "Context:\n%s\n\nQuestion: %s\n\nAnswer:",
            context, question
        );
        
        return openAI.generateText(prompt);
    }
}
```

## 6. **Обработка streaming ответов**

```java
@Service
public class StreamingService {
    public Flux<String> streamChatResponse(String prompt) {
        return webClient.post()
            .uri("/chat/completions")
            .bodyValue(Map.of(
                "model", "gpt-4",
                "messages", List.of(Map.of("role", "user", 
                    "content", prompt)),
                "stream", true
            ))
            .retrieve()
            .bodyToFlux(String.class)
            .map(this::parseStreamChunk);
    }
}
```

## 7. **Кэширование и оптимизация**

```java
@Service
public class CachedLLMService {
    private final RedisTemplate<String, String> redis;
    
    @Cacheable(value = "llm-responses", key = "#prompt")
    public String getCachedResponse(String prompt) {
        return openAIService.generateText(prompt);
    }
    
    // Rate limiting
    @RateLimiter(name = "openai")
    public String rateLimitedCall(String prompt) {
        return openAIService.generateText(prompt);
    }
}
```

## 8. **Мониторинг и observability**

```java
@Service
public class MonitoredLLMService {
    private final MeterRegistry registry;
    
    public String callWithMetrics(String prompt) {
        Timer.Sample sample = Timer.start(registry);
        
        try {
            String response = openAIService.generateText(prompt);
            
            registry.counter("llm.calls", 
                "status", "success").increment();
            registry.summary("llm.tokens.input")
                .record(countTokens(prompt));
                
            return response;
        } catch (Exception e) {
            registry.counter("llm.calls", 
                "status", "error").increment();
            throw e;
        } finally {
            sample.stop(registry.timer("llm.latency"));
        }
    }
}
```

## Ключевые аспекты:

1. **API интеграция** - основной способ (OpenAI, Azure, HuggingFace)
2. **Микросервисная архитектура** - Python сервисы для ML
3. **Векторные БД** - для semantic search (Pinecone, Weaviate)
4. **Кэширование** - экономия на API calls
5. **Async/Streaming** - для real-time ответов
6. **Error handling** - retry logic, fallbacks
7. **Monitoring** - метрики, логи, трейсинг
8. **Cost control** - rate limiting, token counting