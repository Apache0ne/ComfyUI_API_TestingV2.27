# ComfyUI Image Generator Frontend

This project is a React-based frontend for the ComfyUI Image Generator with LLM Integration.

## Prerequisites

- Node.js (v14.0.0 or later)
- npm (v6.0.0 or later)

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/comfyui-react-project.git cd comfyui-react-project/frontend


2. Install dependencies:
npm install


## Running the Application

To start the development server:
npm start


This runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Available Scripts

In the project directory, you can run:

- `npm start`: Runs the app in development mode.
- `npm test`: Launches the test runner in interactive watch mode.
- `npm run build`: Builds the app for production to the `build` folder.
- `npm run eject`: Removes the single build dependency from your project.

## Project Structure

- `src/`: Source files for the React application
  - `components/`: React components
    - `ImageGenerator.js`: Main component for image generation
    - `ModelSelector.js`: Component for model and LoRA selection
    - `PromptInput.js`: Component for prompt input
    - `Setup.js`: Component for LLM setup
  - `App.js`: Main application component
  - `index.js`: Entry point of the React application
  - `api.js`: Functions for API calls to the backend
  - `index.css`: Global styles

## Configuration

The application is configured to proxy API requests to `http://localhost:5000` in development. If your backend is running on a different port, update the `"proxy"` field in `package.json`.

## Contributing

Please read [CONTRIBUTING.md](../CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](../LICENSE.md) file for details.