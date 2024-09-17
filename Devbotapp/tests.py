import re

class CodeExtractor:
    def __init__(self, text):
        self.text = text

    def extract_code(self):
        html_code = re.search(r'(?<=// index.html).*?(?=// styles.css)', self.text, re.DOTALL).group(0).strip()
        css_code = re.search(r'(?<=// styles.css).*?(?=// script.js)', self.text, re.DOTALL).group(0).strip()
        js_code = re.search(r'(?<=// script.js).*', self.text, re.DOTALL).group(0).strip()
        return html_code, css_code, js_code

    def save_code_to_files(self, html_filename, css_filename, js_filename):
        html_code, css_code, js_code = self.extract_code()

        with open(html_filename, 'w') as html_file:
            html_file.write(html_code)

        with open(css_filename, 'w') as css_file:
            css_file.write(css_code)

        with open(js_filename, 'w') as js_file:
            js_file.write(js_code)

# Example usage
text = """
// index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Pages</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header Section -->
    <header>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About Us</a></li>
                <li><a href="#contact">Contact Us</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section id="hero">
        <h1>Welcome to our Website!</h1>
        <p>This is a sample text.</p>
        <button>Learn More</button>
    </section>

    <!-- About Us Section -->
    <section id="about">
        <h2>About Our Company</h2>
        <p>This is a sample text about our company.</p>
        <img src="company-logo.png" alt="Company Logo">
    </section>

    <!-- Contact Us Section -->
    <section id="contact">
        <h2>Contact Us</h2>
        <form>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name"><br><br>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email"><br><br>
            <label for="message">Message:</label>
            <textarea id="message" name="message"></textarea><br><br>
            <input type="submit" value="Send Message">
        </form>
    </section>

    <!-- Footer Section -->
    <footer>
        <p>&copy; 2023 Our Company Name</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>

// styles.css
body {
    font-family: Arial, sans-serif;
}

header nav ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: space-between;
}

header nav li {
    margin-right: 20px;
}

header nav a {
    color: #333;
    text-decoration: none;
}

#hero h1 {
    font-size: 36px;
    margin-bottom: 10px;
}

#hero button {
    background-color: #4CAF50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}

#about img {
    width: 200px;
    height: 100px;
    margin: 20px;
}

#contact form label {
    display: block;
    margin-bottom: 5px;
}

#contact form input[type="text"], #contact form input[type="email"] {
    width: 100%;
    height: 30px;
    margin-bottom: 10px;
    padding: 10px;
    box-sizing: border-box;
    border: 1px solid #ccc;
}

#contact form textarea {
    width: 100%;
    height: 150px;
    margin-bottom: 10px;
    padding: 10px;
    box-sizing: border-box;
    border: 1px solid #ccc;
}

// script.js
document.addEventListener("DOMContentLoaded", function () {
    // Add event listener to submit button
    const submitButton = document.querySelector("#contact form input[type='submit']");
    submitButton.addEventListener("click", function (event) {
        event.preventDefault();
        console.log("Form submitted!");
    });
});
"""

# Instantiate the class and save the code to files
code_extractor = CodeExtractor(text)
code_extractor.save_code_to_files('index.html', 'styles.css', 'script.js')
