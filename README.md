# Design Patterns Used in This Structure

This project is organized based on several common software design patterns that help improve modularity, scalability, and maintainability. Below are the key patterns and how they are applied:

## 1. Layered Architecture

The structure follows a layered architecture, where each layer has its own responsibility:

- **Presentation Layer (API Routes)**: The API routes in `main.py` handle incoming user requests and return the appropriate responses.
- **Service Layer (Business Logic)**: The functions in the `crud/` folder contain business logic and process the requests coming from the Presentation Layer.
- **Persistence Layer (Database)**: The models and database connections are managed within the `models/` and `database/` folders, encapsulating all database-related operations.

## 2. Modular Design

The project is divided into separate modules (e.g., `auth/`, `users/`, `products/`), each representing a specific feature or functionality. This modular approach makes it easier to extend and maintain the application, as changes to one module do not affect the others.

## 3. Singleton Pattern

The use of `SessionLocal` in `database/base.py` to manage database connections demonstrates the **Singleton Pattern**. This ensures that there is only one instance of the session throughout the application's lifecycle, which helps manage database sessions efficiently.

## 4. Factory Pattern

The functions in the `crud/` folder, such as `create_user` and `get_users`, can be seen as implementing the **Factory Pattern**. These functions create and return new objects (e.g., a `User` object) based on specific business logic, abstracting the object creation process from the rest of the code.

---