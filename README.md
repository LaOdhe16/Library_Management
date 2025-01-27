# Library Book Borrowing System

The Library Book Borrowing System is a web-based application developed using Flask and MySQL, designed to streamline the management and borrowing of books in a library. The application features two types of users: Regular Users and Admins. Users can register, log in, borrow available books, view their borrowing history, and return books once finished. On the other hand, Admins have access to add, edit, and delete book data, as well as view the borrowing history of all users. The system also includes a book search feature by title, author, or category. The application offers a responsive design powered by Bootstrap, ensuring a seamless experience across different devices. Additionally, there is a point system that rewards active users. The goal of this system is to make book borrowing management more efficient and facilitate better interaction between users and admins.

## Feature

- **User Authentication**: Users can register and log in to their accounts.
- **User Dashboard**: Displays the user's profile, borrowing history, and the option to view available books.
- **Book Management**: Admins can add, edit, or delete books in the library system. Books have a status (available/borrowed).
- **Borrowing History**: Users can view their borrowing history, while admins can access the borrowing history of all users.
- **Book Return**: Users can return books they have borrowed, updating the book's status and availability.
- **Search Feature**: Users can search for books by title, author, or genre.
- **Responsive Design**: The system is designed to be fully responsive, ensuring a seamless experience across different devices.
- **Admin Features**: Admins have access to manage users and control book inventory.

## Installation

Follow these steps to set up the project locally:

1. Clone this repository:
    ```bash
    git clone <repository_url>
    ```

2. Install dependencies by creating a virtual environment and using `pip`:
    ```bash
    python -m venv venv
    source venv/bin/activate   # For macOS/Linux
    venv\Scripts\activate      # For Windows
    pip install -r requirements.txt
    ```

3. Set up the database connection (MySQL) as per your environment configuration in the `config.py` file.

4. Run migrations (if applicable) to set up the necessary tables in your database.

## Deploy on Vercel

To deploy the application on Vercel, follow these steps:

1. Create an account on [Vercel](https://vercel.com/) if you don't already have one.
2. Connect your GitHub repository to Vercel.
3. Set the environment variables (like database credentials) in the Vercel dashboard.
4. Deploy the application by following the prompts on Vercel.

Once deployed, you can access the live application using the following link:
```bash
[https://library-management-puce-gamma.vercel.app/](https://library-management-8ixn.vercel.app/)




