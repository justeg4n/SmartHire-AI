import boto3
import json

def generate_interview_question(jd_context, conversation_history):
    bedrock = boto3.client(service_name='bedrock-runtime')
    model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
    
    # The System Prompt defines the AI's persona and rules 
    system_prompt = """You are a Senior Technical Recruiter conducting an interview.
    Your goal is to ask ONE highly relevant, challenging technical follow-up question based on the Job Description and the Candidate's last answer.
    
    RULES:
    1. Ask exactly ONE question.
    2. Keep it conversational and natural (under 3 sentences).
    3. DO NOT output JSON. Output only the spoken words of the interviewer.
    4. Base your question strictly on the provided Job Description context."""

    # Construct the user message injecting the RAG context and history
    user_message = f"""
    <job_description_context>
    {jd_context}
    </job_description_context>
    
    <conversation_history>
    {conversation_history}
    </conversation_history>
    
    Based on the context and the history, what is your next question to the candidate?
    """

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 150, # Keep it short for a snappy voice response
        "temperature": 0.7, # Higher temperature (0.7) makes the AI sound more conversational and human
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    print("Generating question via Claude 3.5 Sonnet...")
    response = bedrock.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',
        body=json.dumps(payload)
    )
    
    result = json.loads(response.get('body').read())
    return result['content'][0]['text']

# --- TEST THE FUNCTION ---
if __name__ == "__main__":
    # Simulated RAG Context (What the Knowledge Base retrieved)
    sample_jd_chunk = "The candidate must have deep experience with AWS Serverless architectures, specifically optimizing AWS Lambda cold starts using .NET 8 Native AOT."
    
    # Simulated Conversation History
    sample_history = "Candidate: 'In my last project, I built a microservice using .NET 8 and deployed it to AWS Lambda. It handled our payment processing.'"
    
    next_question = generate_interview_question(sample_jd_chunk, sample_history)
    
    print("\n--- AI INTERVIEWER OUTPUT ---")
    print(next_question)