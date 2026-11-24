# MedGuide AI – Presentation Outline and Viva

## Suggested 10-slide presentation
1. **Title:** MedGuide AI – AI-Powered Healthcare Information and Medicine Awareness Assistant.
2. **Problem:** Health information can be confusing; unconstrained AI can produce unsupported answers.
3. **Objectives:** Educational chatbot, RAG, local LLM, sources, fallback and safety.
4. **Technology stack:** Python, Flask, HTML/CSS/JS, TF-IDF, cosine similarity, Ollama, Llama 3.2:3b.
5. **Architecture:** Browser → Flask → emergency check → retrieval → Ollama → answer and sources.
6. **Dataset:** 35 records, five fields, JSON runtime format and CSV copy, official source links.
7. **RAG workflow:** vectorize records, vectorize question, cosine similarity, top three, context prompt.
8. **Implementation/demo:** ask a supported question; show source cards and relevance scores.
9. **Safety and testing:** disclaimer, emergency bypass, retrieval fallback, pytest suite and limitations.
10. **Conclusion and future scope:** semantic retrieval, expanded reviewed knowledge base, multilingual access and expert evaluation.

## Short demonstration script
"MedGuide AI is an educational healthcare-awareness assistant. When I submit a question, Flask first validates it and checks selected emergency phrases. For a normal question, the TF-IDF retrieval module compares it with the knowledge base using cosine similarity and selects up to three records. These records are passed as context to Llama 3.2 running locally through Ollama. The generated answer and retrieved source links are displayed. If Ollama is unavailable, the application returns the retrieved educational content as a fallback. It does not diagnose or prescribe."

## Viva questions and answers
**1. What is MedGuide AI?**  
It is an educational healthcare information chatbot that demonstrates RAG and local LLM generation.

**2. What is an LLM?**  
A large language model is trained on large text collections to understand prompts and generate natural-language output.

**3. What is RAG?**  
Retrieval-augmented generation retrieves relevant external information and supplies it to an LLM as context before generation.

**4. Why use RAG instead of only an LLM?**  
RAG grounds the response in a selected knowledge base and makes source records visible. It does not guarantee correctness.

**5. What is TF-IDF?**  
Term Frequency–Inverse Document Frequency assigns weights based on a term's frequency in a document and rarity across the corpus.

**6. What is cosine similarity?**  
It measures similarity between vectors using the cosine of the angle between them.

**7. Why retrieve three records?**  
The project requirement is to show the three highest-scoring relevant records as context without overwhelming the prompt.

**8. What does a relevance score mean?**  
It is a text similarity score between the question and a record, not a probability or medical confidence score.

**9. What is Ollama?**  
Ollama provides a local runtime and API for running supported language models on a computer.

**10. Which model is used?**  
Llama 3.2:3b, configured through the `OLLAMA_MODEL` environment variable.

**11. Why use Flask?**  
Flask is a lightweight Python framework suitable for serving the webpage and JSON API endpoints.

**12. What happens if Ollama is offline?**  
The application catches the connection failure and returns a safe answer assembled from retrieved educational records.

**13. How are emergencies handled?**  
A basic phrase check runs before retrieval and LLM generation. A match returns an urgent emergency message immediately. This is not comprehensive triage.

**14. Does the application prescribe medicine?**  
No. It explains general medicine-awareness terminology and directs individual medicine questions to qualified professionals.

**15. Why store JSON and CSV?**  
JSON is easy for Python to load as structured records; CSV is convenient for inspection and spreadsheet tools.

**16. What are the limitations of TF-IDF?**  
It relies on word overlap and may miss semantic similarity, synonyms or different phrasing.

**17. What is the purpose of the fallback?**  
It keeps the educational knowledge base accessible when local LLM generation fails.

**18. What tests are included?**  
Tests cover routes, validation, retrieval, no-match behavior, emergency bypass, fallback and feedback.

**19. Is this ready for real clinical use?**  
No. It is an academic prototype and would require clinical review, safety validation, privacy review and regulatory assessment before any clinical deployment.

**20. What can be improved?**  
Use reviewed and expanded sources, semantic retrieval, multilingual evaluation, better safety testing and expert review.
