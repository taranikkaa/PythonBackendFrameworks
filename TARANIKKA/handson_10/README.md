# Hands-On 10: Microservices Decomposition

## 1. Bounded Context Microservice Mappings (Step 96)
* **Course Service**: Responsible for Course CRUD. Owns `courses.db`. Port 5001.
* **Student Service**: Responsible for Student CRUD and Enrollment actions. Owns `students.db`. Port 5002.
* **API Gateway**: Entry proxy routing request paths to correct services. Port 5000.

## 2. Tradeoffs: Synchronous (HTTP) vs Asynchronous (Message Queue) (Step 104)
* **Synchronous (HTTP)**:
  * *Pros*: Simple to build, clean instant confirmation loops.
  * *Cons*: Heavy architectural coupling. If the Course Service crashes, registrations fail immediately (Error 503).
* **Asynchronous (RabbitMQ / Kafka)**:
  * *Pros*: High resilience. If a target microservice crashes, events sit safely in a message queue until it boots back up.
  * *Cons*: Eventual consistency issues and extra configuration overhead.