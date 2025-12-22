# Naraz Web Application

## 1. Overview

Naraz is a modern multi-vendor e-commerce web application designed to connect customers, shop owners, and administrators on a single scalable platform. The system allows public product browsing, secure customer shopping, shop-based product management, admin-controlled verification, order aggregation, financial transparency, and real-time communication.

Naraz follows a role-based architecture where each user role has clearly defined permissions and responsibilities. The platform is built with a RESTful API design and supports real-time features such as chat and order tracking.

---

## 🚀 2.  Core Features

| #  | Feature                        | Description                                                                                                         |
| -- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| 1  | Public Product & Shop Browsing | Users can explore products and shops without logging in, making it easy to discover offerings.                      |
| 2  | Secure Authentication          | Robust authentication system with email verification and JWT tokens to ensure secure access.                        |
| 3  | Role-Based Access Control      | Four distinct user roles (Admin, Shop Owner, Customer, etc.) with tailored permissions for security and management. |
| 4  | Shop Management System         | Allows shop owners to create and manage their shop efficiently, supporting multiple vendors in the platform.        |
| 5  | Product & Category Management  | Shop owners can add unlimited products and categories, making inventory management simple and organized.            |
| 6  | Advanced Filtering & Search    | Customers can filter products by category, price range, or shop, enabling faster and smarter product discovery.     |
| 7  | Order Management System        | Handles orders from multiple shops, ensuring smooth processing and tracking of all customer purchases.              |
| 8  | Shipping Address Handling      | Customers can save and manage multiple shipping addresses for hassle-free order delivery.                           |
| 9  | Real-Time Order Tracking       | Customers can monitor their order status live, from processing to delivery, for full transparency.                  |
| 10 | Real-Time Chat System          | WebSocket-powered chat system allows instant communication between customers and shop owners.                       |
| 11 | Wallet & Top-Up System         | Shop owners can manage earnings, view balances, and top-up wallets for seamless financial operations.               |
| 12 | Transaction Tracking           | Full tracking of all financial transactions for both customers and shop owners, ensuring transparency.              |
| 13 | Admin Verification System      | Admins can verify shops and products to maintain quality control and ensure trustworthiness.                        |
| 14 | RESTful API Architecture       | Backend designed with RESTful APIs for scalability, flexibility, and easy integration with other services.          |
 

---
 

## User Roles

Naraz has four primary roles:

- **Public User (Visitor)**
- **Customer**
- **Shop Owner**
- **Admin**

---

## 3. Feature Details (Role-Based)

### 3.1 Public (Visitor)

Public users do not need authentication.

#### Capabilities

- View all shops
- View all products
- View product details
- Filter products by:
  - Category
  - Price range
  - Shop name
  - Keywords
- Browse paginated product listings

#### Restrictions

- Cannot add to cart
- Cannot place orders
- Cannot chat

---

### 3.2 Customer

Customers must register and verify their email to unlock full access.

#### Authentication & Verification

- Register account
- Receive OTP/email verification
- Login with JWT authentication
- Unverified users are blocked from ordering

```
Register → Receive OTP → Verify Email → Login (JWT)
```

#### Product Interaction

- View all shops and products
- Add single or multiple products to cart
- Update cart quantities
- Remove items from cart

#### Order Management

- Place orders (single or multiple products)
- Provide shipping address during checkout
- Order contains:
  - Product slug(s)
  - Quantity
  - Shipping address

#### Order Tracking

- View only their own orders
- Track order status in real time
- See per-item status updates

#### Chat System

- Real-time chat with shop owners
- Order-based chat channels
- Message history available

#### Transaction History

- View payment and order history

---

### 3.3 Shop Owner

Shop owners are registered users with extended permissions.

#### Shop Creation & Verification

- Register as a user
- Create only one shop
- Shop requires admin verification before going live

```
Register → Create Shop → Admin Verification → Shop Goes Verifyed
```

#### Product & Category Management

- Create unlimited categories
- Create unlimited products
- Upload multiple product images
- Manage product variants and pricing
- Update or delete products

#### Order Visibility

- Cannot place orders
- Can view orders only for products belonging to their shop
- Track per-item order status
- Update item status:
  - Pending
  - Processing
  - Shipped
  - Delivered

#### Chat System

- Chat with customers for their shop orders
- Respond in real time

#### Wallet & Top-Up System

- Maintain a shop wallet
- Can submit only one bank account information
- Request wallet top-up by:
  - Physical bank payment
  - Uploading receipt
- View top-up status (pending / approved / rejected)

#### Earnings

- View earnings summary
- Track credited balance after admin approval

---

### 3.4 Admin

Admin has full system-level control.

#### Verification Responsibilities

- Verify customer email system
- Verify newly created shops
- Verify shop owner top-up requests

#### Order Aggregation & Distribution

- Collect order items from multiple shop owners
- Combine items into delivery packages
- Distribute final packages to customers

#### Financial Management

- Provide multiple official bank accounts
- Verify shop owner payment receipts
- Approve or reject top-up requests
- Credit verified balance to shop owner wallets

#### Monitoring & Control

- View all users, shops, products, and orders
- Monitor all transactions
- Resolve disputes
- Manage platform integrity

---

## 4. Order System

Customers can place orders for single or multiple products, even from different shops. They must provide a shipping address.

Once placed, orders are **Pending**, and items are automatically assigned to the respective shop owners. Shop owners see and manage only their shop's items, updating status: **Pending → Processing → Shipped → Delivered**.

Customers can track order status in real time. Admin collects items from shop owners and distributes the package. Orders are completed when delivered or canceled if needed. Chat channels between customer and shop owners close automatically after delivery or cancellation.

```
Pending → Processing → Shipped → Delivered
```

---

## 5. Chatting Feature (Customer ↔ Shop Owner)

- Chat is order-based and works in real time
- When a customer places an order with products from one or multiple shops, chat channels are automatically opened
- A separate chat channel is created between:
  - Customer ↔ Each shop owner whose product is in the order
- Chat becomes active when the order status is **Pending**
- Both customer and shop owner can send messages related to the order
- Shop owners can see only chats for their own shop items
- Chat remains open while the order is:
  - Pending
  - Processing
  - Shipped
- Chat is automatically closed when the order is:
  - Delivered
  - Canceled
- After closure, the chat becomes read-only and no new messages can be sent
- Chat is powered by real-time WebSocket communication

---

## 6. Top-Up System (Shop Owner Wallet)

- The platform provides a wallet system for shop owners
- Admin publishes multiple official bank accounts for payments
- A shop owner can add only one bank account to their profile
- To top up balance:
  - Shop owner makes a physical bank payment to an admin-provided bank account
  - Shop owner uploads the payment receipt and submits a top-up request
- Top-up request status:
  - Pending
  - Approved
  - Rejected
- Admin verifies the receipt and bank payment
- After approval:
  - Admin credits the amount to the shop owner's wallet balance
- If rejected:
  - Balance is not updated and the reason may be shown
- Shop owners can track:
  - Wallet balance
  - Top-up history
  - Approval status

---

## 7. API Architecture

- RESTful design
- Strip API Standard
- JWT-based authentication
- Role-based permissions
- Public & private endpoints
- WebSocket support for chat

---

## 8. FAQ – Shop Management System

**Q1: What features are still pending?**  
> A1: Admin needs to collect products and deliver them to customers.

**Q2: When is a chat room created?**  
> A2: A chat room is created when a customer goes to the order details page from the product dashboard and selects the "Talk" option.

**Q3: How many shops can a shop owner create?**  
> A3: A shop owner can create only one shop.

**Q4: How does a shop owner manage products if a customer orders from multiple shops?**  
> A4: Products will be managed separately by each shop owner.

**Q5: When a product is delivered and payment is cash on delivery, where is the balance added?**  
> A5: The balance will be added to the shop owner's account.

**Q6: If the same customer places multiple orders from the same shop in a day, will multiple chat rooms be created or just one?**  
> A6: A separate chat room will be created for each order. If the same customer places multiple orders, multiple chat rooms will exist.

---

## Conclusion

Naraz is a secure, scalable, and role-driven e-commerce platform built to support multi-vendor business models. By combining strong authentication, admin-controlled verification, real-time features, and transparent financial handling, Naraz ensures trust and efficiency for all users.




---
 
> [`Author`](https://github.com/anmamuncoder)
> [`Project`](https://github.com/VTS-learn/team-setu-be.git)

