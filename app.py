from flask import Flask, request, jsonify, render_template
import openai

openai.api_key = ''

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        print("No message provided")
        return jsonify({"error": "No message provided"}), 400
    
    modified_input = f"Please convert the following request into an SQL SELECT query: {user_input}"
    print(f"User input: {user_input}")
    print(f"Modified input for OpenAI: {modified_input}")
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": modified_input}
            ],
            max_tokens=150
        )
        sql_query = response['choices'][0]['message']['content'].strip()

        print(f"SQL Query generated: {sql_query}")

        if sql_query == '':
            return jsonify({"error": "Failed to generate SQL query. Please provide a clearer request."}), 400

        return jsonify({"response": sql_query})

    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)