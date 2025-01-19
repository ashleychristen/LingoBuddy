# LingoBuddy
## Project Overview
The Endangered Language Learning Elmo is a conversational AI-powered toy designed to preserve endangered languages by teaching children their native language in a fun and engaging way. This interactive tool allows children to converse with Elmo, who listens, translates, and responds in both English and the selected endangered language. Additionally, it leverages facial emotion recognition to make Elmo’s responses more empathetic and tailored to the child’s emotional state.

## How It Works
### Program Flow
1. **Language Selection**:
  - When the program is run, Elmo asks the child what language they want to learn or speak.
2. **Speech Recognition**:
  - The child speaks to Elmo in English.
  - Using Google Cloud Speech-to-Text, the spoken words are transcribed into text.
3. **Language Translation**:
  - The transcribed text is sent to the OpenAI API, which translates it into the selected language.
4. **Conversational Response**:
- Elmo repeats the child’s message in the chosen language.
- E  lmo also responds to the child in both English and the selected language, ensuring comprehension while encouraging language learning.
5. **Text-to-Speech Conversion**:
  - Responses are converted into audio using SpeechGen.io to give Elmo a realistic voice in whatever language being spoken.
6. **Facial Emotion Recognition**:
  - Using an open-source facial emotion recognition repository, the child’s emotions are analyzed in real-time.
  - Elmo adapts his responses based on the child’s detected emotional state (e.g., using a more encouraging tone if the child seems frustrated).

## Technologies Used
**Google Cloud Speech-to-Text**: For transcribing the child’s spoken words into text.

**OpenAI API**: For translating the child’s text and generating appropriate responses.

**SpeechGen.io**: For converting Elmo’s responses into spoken audio.

**OpenCV** + **DeepFace**: For real-time facial emotion recognition.

## Key Features
**Language Learning**:
- Encourages conversational practice in endangered languages.
- Provides immediate translation and responses to immerse children in the language.
**Emotionally Intelligent Responses**:
- Analyzes the child’s facial expressions to detect emotions such as happiness, sadness, or frustration.
- Tailors Elmo’s tone and response to create a more engaging and empathetic experience.
**Bilingual Feedback**:
- Combines English and the selected language in responses to enhance understanding and encourage learning.
