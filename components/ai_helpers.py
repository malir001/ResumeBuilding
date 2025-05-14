import openai

def ai_generate_experience(role, industry, tasks=""):
    prompt = f"""You are an expert resume writer. Create 3 impactful, ATS-optimized bullet points for a {role} working in a {industry} environment.
Use keywords relevant to that industry and role. {f'Incorporate these tasks if helpful: {tasks}' if tasks else ''}"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response['choices'][0]['message']['content']
