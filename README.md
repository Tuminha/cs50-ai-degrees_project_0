# 🎬 Six Degrees of Kevin Bacon 🎬

![Six Degrees of Kevin Bacon App](https://github.com/Tuminha/cs50-ai-degrees_project_0/blob/main/images/six_degrees_of_Kevin_Bacon.png)

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)
- [Algorithm](#algorithm)
- [Live Demo](#live-demo)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

The "Six Degrees of Kevin Bacon" project is an interactive web application that demonstrates the famous "Six Degrees of Separation" theory in the context of the film industry. This app allows users to find the shortest connection between any two actors through the movies they've starred in, with a special focus on connecting actors to Kevin Bacon.

This project was developed as part of the CS50 Introduction to Artificial Intelligence with Python course from Harvard University. It showcases the implementation of graph search algorithms (Breadth-First Search and Depth-First Search) to find connections in a complex network of actors and movies.

![Example of Result in Streamlit App](https://github.com/Tuminha/cs50-ai-degrees_project_0/blob/main/images/example_of_result_in_streamlit_app.png)

## ✨ Features

- Choose between small and large datasets of actors and movies
- Input any two actors to find their connection
- Visualize the degrees of separation with an interactive bar chart
- Compare the performance of BFS and DFS algorithms
- User-friendly interface with emoji enhancements
- Responsive design for various screen sizes

## 🚀 Installation

To run this project locally, follow these steps:

1. Clone the repository:
git clone https://github.com/Tuminha/six-degrees-of-kevin-bacon.git
cd six-degrees-of-kevin-bacon
Copy
2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Copy
3. Install the required packages:
pip install -r requirements.txt
Copy
## 🖥️ Usage

To run the Streamlit app locally:
streamlit run app.py
Copy
Navigate to the URL provided in the terminal (usually `http://localhost:8501`).

To use the command-line version:
python degrees.py [directory]
Copy
Replace `[directory]` with either `small` or `large` to specify which dataset to use.

## 📁 File Structure
.
├── README.md
├── app.py
├── degrees.py
├── util.py
├── requirements.txt
├── large
│   ├── movies.csv
│   ├── people.csv
│   └── stars.csv
└── small
├── movies.csv
├── people.csv
└── stars.csv
Copy
- `app.py`: Streamlit web application
- `degrees.py`: Core logic for finding connections between actors
- `util.py`: Utility classes for graph search algorithms
- `requirements.txt`: List of Python dependencies
- `large/` and `small/`: Datasets containing movie and actor information

## 🛠️ Technologies Used

- Python 3.9+
- Streamlit 1.37.1
- pandas
- numpy
- alive-progress

## 🧠 Algorithm

The project implements two graph search algorithms:

1. **Breadth-First Search (BFS)**: Guarantees the shortest path between two actors.
2. **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking.

Both algorithms are run concurrently, allowing for performance comparison. The application uses a graph representation where actors are nodes and movies are edges connecting the actors.

## 🌐 Live Demo

Experience the Six Degrees of Kevin Bacon app live at: [https://degrees.streamlit.app/](https://degrees.streamlit.app/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Developed with ❤️ by Francisco Teixeira Barbosa

📧 Email: cisco@periospot.com
🐦 Twitter: [@cisco_research](https://twitter.com/cisco_research)
📷 Instagram: [Tuminha_dds](https://www.instagram.com/Tuminha_dds)
🌐 Website: [periospot.com](https://periospot.com)