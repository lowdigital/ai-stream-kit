![DEMO](demo.jpg)


# AI STREAM KIT: AI Scenarios for SpongeBob

AI STREAM KIT is a comprehensive project designed to organize AI-generated voiceovers for SpongeBob scenarios. Leveraging advanced technologies like RVC (Retrieval-based Voice Conversion) and RVC TTS (Text-to-Speech), this toolkit automates the creation of engaging and dynamic content for SpongeBob enthusiasts and content creators.

## Table of Contents

1. Features
2. Technologies Used
3. Installation
    - Prerequisites
    - Cloning the Repository
    - Installing Dependencies
4. Configuration
    - Environment Variables
    - Setting Up RVC and RVC TTS
5. Usage
    - Running the Controllers
    - Starting the Web Servers
    - Monitoring Live Chat for Commands
6. Project Structure
7. Troubleshooting
8. Contributing
9. License

## Features

- **Automated Scenario Generation:** Creates comedic dialogues between SpongeBob and other characters based on user-provided topics.
- **Text-to-Speech Integration:** Utilizes RVC TTS to generate voiceovers for each character's dialogue.
- **Audio Mashup Creation:** Downloads and processes YouTube audio to create mashups with the generated voiceovers.
- **Live Chat Monitoring:** Listens to live chat messages for commands like `/skip` to manage scenario flow.
- **API Integration:** Communicates with external APIs to fetch and push scenario data.
- **Error Handling and Logging:** Comprehensive logging with colored console messages for easy debugging.

## Technologies Used

- **Programming Language:** Python 3.7+
- **Web Frameworks:**
  - `aiohttp` for asynchronous web server in `controller.py`.
  - `Flask` for API endpoints in `gateway.py`.
- **Audio Processing:**
  - `pydub` for audio manipulation.
  - `moviepy` for handling audio clips.
- **YouTube Handling:**
  - `pytubefix` for downloading and processing YouTube audio.
- **Live Chat Monitoring:**
  - `pytchat` for interacting with YouTube live chats.
- **Other Libraries:**
  - `requests`, `asyncio`, `random`, `string`, `datetime`, `re`, `json`, etc.

## Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Operating System:** Windows 10 or later / Linux / macOS
- **Python Version:** Python 3.7 or higher
- **Dependencies:** Git, pip
- **External Tools:**
  - RVC: [Installation Guide](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
  - RVC TTS: [Installation Guide](https://github.com/litagin02/rvc-tts-webui)
  - Gradio: Ensure Gradio app is running on `http://127.0.0.1:7860/`

### Cloning the Repository

```bash
git clone https://github.com/your-username/ai-stream-kit.git
cd ai-stream-kit
```

### Installing Dependencies

It's recommended to use a virtual environment to manage dependencies.

1. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment:**

   - Windows:

     ```bash
     venv\Scripts\activate
     ```

   - macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory of the project to store your configuration variables. Here's an example:

```env
API_DOMAIN=https://your-api-domain.com
GRADIO_PATH=C:\Users\admin\AppData\Local\Temp\gradio
STREAM_ID=YOUR_YOUTUBE_STREAM_ID
PROXY=http://USERNAME:PASSWORD@IP:PORT
API_DEBUG=True
```

### Setting Up RVC and RVC TTS

Ensure that both RVC and RVC TTS services are running locally on the specified ports (7897 for RVC and 3000 for RVC TTS).

1. **RVC Setup:** Follow the RVC Installation Guide to install and run the RVC service.
2. **RVC TTS Setup:** Follow the RVC TTS Installation Guide to install and run the RVC TTS service.
3. **Gradio App:** Ensure that the Gradio application is running on `http://127.0.0.1:7860/`. Follow the Gradio setup instructions if needed.

## Usage

### Running the Controllers

The project consists of three main Python scripts:

- `controller.py`: Handles scenario generation and API interactions.
- `gateway.py`: Manages voice generation and audio mashups.
- `skip.py`: Monitors live chat for skip commands.

#### Starting `controller.py`

```bash
python controller.py
```

**Description:** Starts the aiohttp web server on port 3001 and begins the scenario generation loop.

#### Starting `gateway.py`

```bash
python gateway.py
```

**Description:** Launches the Flask server on port 3000 to handle voice and mashup generation requests.

#### Starting `skip.py`

```bash
python skip.py
```

**Description:** Initiates the live chat monitoring script to listen for `/skip` commands in YouTube live chats.

### Starting the Web Servers

Ensure that both `controller.py` and `gateway.py` are running simultaneously as they communicate with each other and external APIs to function correctly.

### Monitoring Live Chat for Commands

The `skip.py` script listens to your specified YouTube live stream's chat. When a user types `/skip`, it sends a request to the API to skip the current scenario.

**Usage:**

1. Ensure your YouTube live stream is active.
2. Start the `skip.py` script.
3. The script will continuously monitor chat messages for the `/skip` command.

## Project Structure

```plaintext
ai-stream-kit/
├── controller.py
├── gateway.py
├── skip.py
├── requirements.txt
├── README.md
└── downloads/
    └── [Automatically generated download folders]
```

- `controller.py`: Manages scenario generation and serves API endpoints for scenarios.
- `gateway.py`: Handles voice generation and audio mashup processes.
- `skip.py`: Monitors YouTube live chat for user commands.
- `requirements.txt`: Lists all Python dependencies.
- `downloads/`: Directory where downloaded YouTube audio files are stored.

## Troubleshooting

### Common Issues:

1. **Port Conflicts:** Ensure that ports 3000, 3001, and 7860 are not in use by other applications.
2. **API Connectivity:** Verify that `API_DOMAIN` is correctly set and the API services are accessible.
3. **RVC Services:** Ensure RVC and RVC TTS services are running and reachable at their respective ports.
4. **Proxy Settings:** If you're using proxies, ensure they're correctly configured in `gateway.py`.

### Debugging:

- Check console logs for colored messages indicating the status and any errors.
- Use `API_DEBUG=True` in `controller.py` to enable detailed API response logging.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure your code follows the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the MIT License.

## Contacts

Follow updates on the Telegram channel: [low digital](https://t.me/low_digital).
