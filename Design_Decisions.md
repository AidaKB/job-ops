## Design Decisions

### Custom User Model
A `CustomUser` model was implemented by extending Django’s `AbstractUser` and `PermissionsMixin`. This choice ensures flexibility for role-based access control while maintaining compatibility with Django’s authentication system. Three distinct roles were defined: **Admin**, **Technician**, and **Sales Agent**. These roles drive authorization logic throughout the system. For instance, Admins have full system control, while Technicians and Sales Agents interact with job- and client-related features in more limited scopes. Helper methods (`is_admin`, `is_technician`, `is_sales`) were added for readability and to simplify role checks in views and permissions.

### Equipment Model
The `Equipment` model provides a centralized catalog of tools and machines used across jobs. It includes attributes such as `type`, `serial_number`, and activation state. By abstracting equipment into its own entity, the system enables efficient reuse across multiple tasks, ensures better inventory tracking, and supports future extensions such as maintenance history or availability management.

### Job and Task Modeling
The `Job` model represents a client-facing assignment with attributes for scheduling, priority, and lifecycle status. Each job is tied to a creator and optionally assigned to a technician, ensuring accountability and traceability. A job cannot transition to the **Completed** state until all of its tasks are finished, enforcing a strict workflow.

Tasks are encapsulated in the `JobTask` model. Each task has its own lifecycle, ordered execution, and can be associated with one or more pieces of required equipment through a many-to-many relationship. This structure ensures modular breakdown of complex jobs, supports fine-grained tracking, and enables reporting such as average completion time or equipment utilization.

The `save` logic within `JobTask` enforces automatic timestamping when tasks are completed and propagates completion status to the parent job when all tasks are resolved. This design reduces manual overhead and ensures data consistency between tasks and their jobs.

### Workflow and Priority
The use of enumerated choices (`Status`, `Priority Levels`) across models enforces controlled state transitions and avoids inconsistent data entry. Priorities allow the scheduling system to rank jobs effectively, while task ordering ensures execution follows a logical sequence.

### Extensibility and Maintainability
The system was designed with extensibility in mind. Role-based users, task-equipment relationships, and job-task workflows can be easily expanded with additional features such as analytics dashboards, overdue job detection (via Celery), or integration with external CRMs. The chosen abstractions keep the codebase modular, readable, and adaptable to new requirements.

---
