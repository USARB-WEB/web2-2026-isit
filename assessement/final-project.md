# 🎓 Final Project: Requirements & Milestones

Welcome to the final project guidelines. This document outlines the core objectives, deliverables, and development phases required to successfully complete your final assignment.

The project simulates a real-world software development lifecycle. You will build a backend application (preferably using **NestJS**) following architectural best practices, modularity, proper database integration, and modern containerization practices.

---

## 📋 Table of Contents
1. [Phase 1: Project ToR & Database Schema](#phase-1-project-tor--database-schema)
2. [Phase 2: Linked CRUD Modules (In-Memory)](#phase-2-linked-crud-modules-in-memory)
3. [Phase 3: Intermediate Project Status 1](#phase-3-intermediate-project-status-1)
4. [Phase 4: Practical Assessment Nr 1 - DB Integration](#phase-4-practical-assessment-nr-1---db-integration)
5. [Phase 5: Practical Assessment Nr 2 - Custom Features](#phase-5-practical-assessment-nr-2---custom-features)
6. [Phase 6: Application Containerization (Docker)](#phase-6-application-containerization-docker)
7. [Phase 7: Pre-Final Project Status 2](#phase-7-pre-final-project-status-2)
8. [💯 Grading System](#-grading-system)

---

## Phase 1: Project ToR & Database Schema
**Objective:** Define the project scope, core objectives, and data architecture.

* **Terms of Reference (ToR):** You must create a ToR document detailing the project's objectives, functional requirements, and the problem it aims to solve. This will serve as your development roadmap.
* **Database Schema:** Design a relational database schema that effectively represents the entities and relationships in your project.
  > ⚠️ **Requirement:** The database diagram must be created using [dbdiagram.io](https://dbdiagram.io/).

**Deliverables:** ToR document + Link/Export of the database diagram.

---

## Phase 2: Linked CRUD Modules (In-Memory)
**Objective:** Establish the backend architecture, routing, and controller logic.

You must initialize a backend project that includes linked CRUD (Create, Read, Update, Delete) modules for managing related entities (e.g., `Study Groups` and `Students`). 

* **Framework:** **NestJS** is highly recommended, though other backend languages or frameworks are permitted.
* **Data Storage:** For this phase, operations should be fully functional using *in-memory data structures* (arrays/objects) without a real database.
* **Architecture:** The project must be structured for easy expansion and maintenance, strictly following code organization and modularity best practices.

---

## Phase 3: Intermediate Project Status 1
**Objective:** Project tracking and blocker identification.

Submit a status update detailing your progress. The goal is to ensure the project is on track and to identify areas requiring additional architectural guidance.

**Include the following in your report:**
- Summary of completed tasks.
- Ongoing work and next steps.
- Any technical challenges or bottlenecks encountered.
- Adjustments made to the original ToR (if any).

---

## Phase 4: Practical Assessment Nr. 1 - DB Integration
**Objective:** Implement data persistence and relational mapping.

During this assessment, you will upgrade the in-memory linked CRUD modules from Phase 2 to interact with a real database. 
* The implementation must accurately reflect the DB schema designed in Phase 1.
* All CRUD operations must persist data correctly.
* Entity relationships (e.g., One-to-Many between Study Groups and Students) must be properly handled by the ORM/Query Builder.
  > 🐳 **Infrastructure Requirement:** The database instance (e.g., PostgreSQL, MySQL) MUST be provisioned and run using **Docker**.

---

## Phase 5: Practical Assessment Nr. 2 - Custom Features
**Objective:** Implement complex business logic beyond standard CRUD.

Enhance your database-backed project by developing custom, real-world features. Examples include, but are not limited to:
- User authentication and authorization.
- Data aggregation endpoints (e.g., displaying grouped data about sales by month).
- Analytical endpoints (e.g., aggregated data about sales by product).
- Transactional processes (e.g., a product ordering or enrollment endpoint).

---

## Phase 6: Application Containerization (Docker)
**Objective:** Package the application for consistent deployment and environment parity.

Modern applications require isolated and reproducible environments. In this phase, you will containerize your entire stack.
* **Application Image:** Write a `Dockerfile` to package your backend application (e.g., NestJS) into a custom Docker image.
* **Orchestration:** Provide a `docker-compose.yml` file that defines and runs both your application container and your database container simultaneously. The entire project should start up using a single `docker-compose up` command.

---

## Phase 7: Pre-Final Project Status 2
**Objective:** Final review before project defense.

Provide a comprehensive pre-final status update on your project. This is the last check-in before the final submission.

**Include the following:**
- Progress made since the first intermediate update.
- Unresolved bugs or challenges (including any Docker-related networking issues).
- The final steps planned to reach completion.
- Confirmation that all features align with the original/updated ToR.

---

## 💯 Grading System
Throughout the development lifecycle, you will receive **5 separate grades** corresponding to critical project milestones. 

* **Grade 1: Project Planning & Database Design (Phase 1)**
  * Evaluates the clarity and completeness of the Terms of Reference (ToR) and the logical correctness of the dbdiagram.io relational schema.
* **Grade 2: Initial API Architecture & Modularity (Phases 2 & 3)**
  * Evaluates the framework initialization (NestJS structure), correct implementation of RESTful principles, in-memory CRUD logic, code cleanliness, and the timely submission of Status Report 1.
* **Grade 3: Practical Assessment Nr. 1 (Phase 4)**
  * Evaluates the successful integration of the ORM/Query builder, accurate reflection of the Phase 1 DB schema, functioning relational queries, and the ability to run the database via Docker.
* **Grade 4: Practical Assessment Nr. 2 (Phase 5)**
  * Evaluates the complexity, functionality, and security of the custom features (e.g., authentication, complex aggregations, or transactional logic).
* **Grade 5: Infrastructure & Final Delivery (Phases 6 & 7)**
  * Evaluates the correct implementation of the `Dockerfile` and `docker-compose.yml`, ensuring the whole stack runs seamlessly. This grade also includes the final code quality review, Status Report 2, and project defense.