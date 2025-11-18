# Online-Book-Store
A featured Django-based online bookstore application with admin management, user authentication, shopping cart functionality, and transaction history tracking. This project is hosted on AWS Elastic Beanstalk with a robust and secure VPC-based architecture, leveraging RDS for the database and an Application Load Balancer (ALB) for high availability.

**Features**
User Management: Register, login, logout.
Admin Panel: CRUD operations on books, view transaction history, and print reports.
Book Catalog: Browse books, add to cart, checkout.
Transaction History: Track purchases with the ability to print invoices.
Secure Deployment: Hosted in a private network with restricted access and HTTPS support.

**AWS Services Used**
Elastic Beanstalk – Hosts Django app with autoscaling EC2 instances.
RDS (PostgreSQL) – Managed database in a private subnet.
VPC – Single VPC with public and private subnets for high availability and security.
Subnets –
    Public Subnet A & B: Hosts ALB and NAT Gateway.
    Private Subnet: Hosts EC2 instances and RDS.
Internet Gateway – Allows public subnets to access the Internet.
NAT Gateway – Enables private instances to fetch updates/pip packages.
Application Load Balancer (ALB) – Routes traffic to EC2 instances and enables HTTPS.
Security Groups – Control inbound/outbound traffic:
    ALB SG: HTTP/HTTPS from anywhere (0.0.0.0/0).
    EC2 SG: Accepts traffic only from ALB SG.
    RDS SG: Accepts traffic only from EC2 SG.

**Database Configuration**
Engine: PostgreSQL
Host: RDS Endpoint in private subnet
User & Password: Configured via environment variables
Port: 5432
Security: RDS accessible only from EC2 instances inside private subnet.

**Security**
EC2 instances in private subnets (recommended) for enhanced security.
ALB in public subnets handles incoming traffic securely.
All sensitive ports blocked externally except HTTP/HTTPS and internal DB access.
NAT Gateway allows outbound Internet access from private subnets for updates.

**Usage**
Admin Panel: /admin – manage books, view transactions.
Home Page: Browse books.
Cart Page: Add/remove items, checkout.
Transactions: View and print purchase history.
Login/Register: User authentication for a personalized experience.

**Future Improvements**
Enable HTTPS using ALB SSL certificates.
Implement multi-AZ RDS for high availability.
Add email notifications for orders.
Add caching (Redis/ElasticCache) for faster performance.
Extend private subnets per AZ for HA and better fault tolerance.
