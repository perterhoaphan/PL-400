# PL-400: Microsoft Power Platform Developer
## Skills measured as of March 19, 2026

---

## Audience Profile

As a candidate for this exam, you design, develop, test, and troubleshoot solution components using the extension points of Microsoft Power Platform. Your expertise encompasses implementing:

- Custom user experiences and business logic
- System integrations
- Data conversions
- Custom process automation
- Complex Power Fx logic
- Power Automate workflow expressions
- AI as part of your solution logic

You must have applied knowledge of:

- Microsoft Power Platform services, including in-depth understanding of its capabilities, boundaries, and constraints
- Authentication, security, and application lifecycle management (ALM) practices for the Microsoft Power Platform
- Microsoft Power Platform developer tools including Power Platform CLI as part of the developer workflow
- AI tools, including agents, to improve development and troubleshooting solutions

As a candidate, you should have development experience that includes Microsoft Power Platform services, JavaScript, JSON, TypeScript, C#, HTML, RESTful Web APIs, Visual Studio, Visual Studio Code, and Microsoft Azure.

---

## Skills at a Glance

| Domain | Weight |
|---|---|
| Create a technical design | 10–15% |
| Build Power Platform solutions | 10–15% |
| Implement Power Apps improvements | 10–15% |
| Extend the user experience | 10–15% |
| Extend the platform | 30–35% |
| Develop integrations | 10–15% |

---

## Domain 1: Create a Technical Design (10–15%)

### Design Technical Architecture
- Analyze the technical architecture to identify solution components and their implementation approach
- Design the authentication and authorization strategy for solution components
- Determine whether requirements can be met with out-of-the-box functionality
- Determine where to implement business logic including cloud computing, client-side processing, business rules, plug-ins, and Power Automate
- Determine when to use standard tables, virtual tables, elastic tables, or connectors
- Assess the impact of Microsoft Power Platform security features on solution components including data loss prevention (DLP) policies, security roles, teams, business units, and row sharing

### Design Solution Components
- Design Power Apps reusable components including canvas components, code components (Power Apps component framework), and client scripting
- Design custom connectors
- Design Dataverse code components including Power Fx functions, plug-ins, and custom APIs
- Design automations including Power Automate cloud flows
- Design inbound and outbound integrations using Dataverse and Azure

---

## Domain 2: Build Power Platform Solutions (10–15%)

### Configure and Troubleshoot Microsoft Power Platform
- Troubleshoot operational security issues
- Configure Dataverse security roles to support code components including the principle of least privilege
- Manage Microsoft Power Platform environments for development

### Implement Application Lifecycle Management (ALM)
- Manage solution dependencies
- Create and use environment variables
- Manage solution layers
- Implement and extend Power Platform Pipelines
- Create Continuous Integration/Continuous Deployment (CI/CD) automations using Power Platform Build Tools

---

## Domain 3: Implement Power Apps Improvements (10–15%)

### Implement Advanced Canvas Apps Features
- Implement complex Power Fx formulas and functions
- Build reusable component libraries
- Utilize Power Automate cloud flows to implement business logic from a canvas app

### Optimize and Troubleshoot Apps
- Troubleshoot canvas and model-driven app issues by using Monitor and other browser-based debugging tools
- Optimize canvas app performance including pre-loading data and query delegation
- Optimize model-driven app performance including forms and views

---

## Domain 4: Extend the User Experience (10–15%)

### Apply Business Logic in Model-Driven Apps Using Client Scripting
- Build JavaScript code that targets the Client API object model
- Determine event handler registration approach
- Create client scripting that targets the Dataverse Web API
- Configure commands and buttons using Power Fx and JavaScript
- Implement navigation to custom pages using the Client API

### Create a Power Apps Component Framework (PCF) Code Component
- Demonstrate the use of the different lifecycle events
- Configure a code component manifest
- Implement component interfaces
- Package, deploy, and consume a component
- Configure and use Device, Utility, and Web API features in component logic

---

## Domain 5: Extend the Platform (30–35%)

### Create a Dataverse Plug-in
- Demonstrate the use of the different event execution pipeline stages
- Develop a plug-in that uses the execution context
- Develop a plug-in that implements business logic
- Implement Pre Images and Post Images to support plug-in logic
- Perform operations in plug-ins by using the Organization service
- Optimize plug-in performance
- Configure a Dataverse custom API message
- Register plug-in components by using the Plug-in Registration Tool
- Develop a plug-in that implements a custom API
- Configure Dataverse business events

### Create Custom Connectors
- Create an Open API definition for an existing REST API
- Implement authentication for custom connectors
- Configure policy templates to modify connector behavior at runtime
- Import definitions from existing APIs including Open API definitions, Azure services, and GitHub
- Create a custom connector for an Azure service
- Develop an Azure Function to be used in a custom connector
- Extend the Open API definition for a custom connector
- Develop code for a custom connector to transform data

### Use Platform APIs
- Perform operations with the Dataverse Web API
- Perform operations with the Organization service
- Implement API limit retry policies
- Optimize for performance, concurrency, transactions, and bulk operations
- Perform authentication by using OAuth

### Process Workloads by Using Azure Functions
- Process long-running operations by using Azure Functions for Microsoft Power Platform solutions
- Implement scheduled and event-driven triggers in Azure Functions for Microsoft Power Platform solutions
- Authenticate to Microsoft Power Platform by using managed identities

### Configure Power Automate Cloud Flows
- Configure Dataverse connector actions and triggers
- Implement complex expressions in flow steps
- Manage sensitive input and output parameters
- Utilize Azure Key Vault
- Implement flow control actions including error handling
- Configure trigger filter and retry policies
- Develop reusable logic by using child flows
- Implement Microsoft Entra ID service principles

---

## Domain 6: Develop Integrations (10–15%)

### Publish and Consume Dataverse Events
- Publish a Dataverse event by using the IServiceEndpointNotificationService
- Publish a Dataverse event by using the Plug-in Registration Tool
- Register service endpoints including webhooks, Azure Service Bus, and Azure Event Hub
- Recommend options for listening to Dataverse events

### Implement Data Synchronization with Dataverse
- Perform data synchronization by using change tracking
- Develop code that utilizes alternate keys
- Utilize the UpsertRequest message to synchronize data

---

## Question Creation Rules (Quy tắc ra đề)

> Tất cả câu hỏi trong database phải tuân thủ nghiêm ngặt các quy tắc sau.

### 1. Cấu trúc JSON bắt buộc

Mỗi câu hỏi phải có đủ các trường sau trong file `questions.json`:

```json
{
  "id": 1,
  "category": "Extend the Platform",
  "type": "single",
  "question": "Nội dung câu hỏi rõ ràng, không mơ hồ?",
  "options": ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"],
  "correct": [0],
  "explanation": "Giải thích tại sao đáp án này đúng và các đáp án khác sai."
}
```

### 2. Các loại câu hỏi (type)

| Type | Mô tả | Số đáp án đúng | Ghi chú |
|---|---|---|---|
| `single` | Chọn một đáp án duy nhất | Đúng 1 | Đề bài không cần ghi chú |
| `multi` | Chọn nhiều đáp án | Từ 2 trở lên | Đề bài **phải** ghi rõ "(Select TWO)" hoặc "(Select THREE)" |

### 3. Danh mục câu hỏi (category) — bắt buộc dùng đúng tên

| category (JSON) | Domain tương ứng |
|---|---|
| `"Technical Design"` | Domain 1: Create a technical design |
| `"Build Solutions"` | Domain 2: Build Power Platform Solutions |
| `"Power Apps"` | Domain 3: Implement Power Apps improvements |
| `"User Experience"` | Domain 4: Extend the user experience |
| `"Extend the Platform"` | Domain 5: Extend the platform |
| `"Integrations"` | Domain 6: Develop integrations |

### 4. Phân bổ câu hỏi theo domain (mỗi bài thi 50 câu)

| Domain | Tỷ lệ đề thi | Số câu trong 50 câu | Số câu tối thiểu trong DB |
|---|---|---|---|
| Technical Design | 10–15% | 5–8 câu | ≥ 20 câu |
| Build Solutions | 10–15% | 5–8 câu | ≥ 20 câu |
| Power Apps | 10–15% | 5–8 câu | ≥ 20 câu |
| User Experience | 10–15% | 5–8 câu | ≥ 20 câu |
| Extend the Platform | 30–35% | 15–18 câu | ≥ 50 câu |
| Integrations | 10–15% | 5–8 câu | ≥ 20 câu |

### 5. Quy tắc chỉ số đáp án (correct)

- Chỉ số **0-based**: đáp án đầu tiên trong `options` là `0`, thứ hai là `1`, v.v.
- Ví dụ: nếu đáp án đúng là đáp án thứ 3, `"correct": [2]`
- Với câu hỏi multi: `"correct": [0, 2]` (chọn đáp án 1 và 3)

### 6. Quy tắc viết câu hỏi

- **Ngôn ngữ**: Câu hỏi viết bằng **Tiếng Anh** (theo format đề thi Microsoft thực tế)
- **Phong cách**: Scenario-based — mô tả tình huống thực tế rồi hỏi giải pháp
- **Không trùng lặp**: Mỗi câu hỏi phải có nội dung khác nhau, không copy-paste
- **Độ khó**: Kết hợp câu dễ (nhớ khái niệm), câu trung bình (hiểu áp dụng), câu khó (phân tích, so sánh)
- **Số options**: Luôn có **4 đáp án** (A, B, C, D) cho câu single; có thể 4–5 đáp án cho câu multi
- **Distractors**: Các đáp án sai phải hợp lý, không quá lộ liễu

### 7. Quy tắc viết explanation

- Giải thích **tại sao đáp án đúng là đúng**
- Có thể đề cập ngắn gọn lý do đáp án sai
- Tham chiếu đến tài liệu Microsoft khi cần
- Độ dài: 1–3 câu

### 8. Keyword quan trọng cần có trong database

Các keyword sau đây **phải xuất hiện** trong ít nhất một câu hỏi:

**Plug-in & Platform:**
- `PreValidation`, `PreOperation`, `PostOperation`
- `IPluginExecutionContext`, `IOrganizationService`, `ITracingService`
- `PreEntityImages`, `PostEntityImages`, `SharedVariables`, `OutputParameters`
- `ExecuteTransactionRequest`, `ExecuteMultipleRequest`
- `RemoteExecutionContext`, `IServiceEndpointNotificationService`
- `Plugin Registration Tool`, `Custom API`, `Business Events`

**PCF (Power Apps Component Framework):**
- `init()`, `updateView()`, `destroy()`, `getOutputs()`
- `ComponentFramework.Context`, `ComponentFramework.PropertyTypes`
- `pac pcf init`, `pac pcf push`, `npm run build`
- `ControlManifest.Input.xml`

**Web API & Organization Service:**
- `Prefer: odata.track-changes`, `Prefer: odata.maxpagesize`
- `$select`, `$filter`, `$expand`, `$orderby`
- `ADAL`, `MSAL`, `OAuth 2.0`
- `UpsertRequest`, `Alternate Keys`
- `CORS`, `Cross-Origin Resource Sharing`

**Power Automate:**
- `outputs()`, `triggerBody()`, `triggerOutputs()`
- `Azure Key Vault`, `child flows`
- `Managed Identity`, `Service Principal`
- `Error handling`, `retry policy`

**ALM & DevOps:**
- `pac solution init`, `pac auth create`, `pac solution export`
- `environment variables`, `solution layers`
- `Power Platform Build Tools`, `CI/CD pipeline`
- `managed solution`, `unmanaged solution`

**Canvas App:**
- `Delegation`, `ClearCollect`, `Concurrent`
- `Monitor tool`, `App.OnStart`, `App.Formulas`
- `Power Fx`, `component library`

### 9. Randomization khi làm bài

Khi user bắt đầu làm bài, hệ thống sẽ:
1. Lấy toàn bộ câu hỏi từ database (`questions.json`)
2. **Random** ngẫu nhiên **50 câu** từ pool (nếu DB có ≥ 50 câu)
3. Thứ tự câu hỏi được xáo trộn ngẫu nhiên
4. Thứ tự các đáp án (options) **không** bị xáo trộn (giữ nguyên A/B/C/D)
5. Mỗi lần làm bài là một session mới với bộ câu hỏi khác nhau

### 10. Passing Score

- Điểm đậu: **700/1000** (tương đương **70%** trên thang điểm scaled, thường ~80% số câu đúng)
- Thời gian: **120 phút** cho 50 câu
- Kết quả hiển thị ngay sau khi nộp bài

---

## Key Technologies & Keywords Reference

### Power Platform CLI (PAC CLI)
| Command | Mục đích |
|---|---|
| `pac auth create` | Tạo kết nối xác thực đến environment |
| `pac auth list` | Liệt kê các profile xác thực |
| `pac pcf init` | Khởi tạo PCF project mới |
| `pac pcf push` | Deploy PCF control lên environment |
| `pac solution init` | Khởi tạo solution project |
| `pac solution export` | Export solution |
| `pac solution import` | Import solution |

### Plug-in Execution Pipeline
| Stage | ID | Mô tả |
|---|---|---|
| PreValidation | 10 | Trước validation, có thể rollback transaction |
| PreOperation | 20 | Trước core operation, trong transaction |
| MainOperation | 30 | Core operation (chỉ internal) |
| PostOperation | 40 | Sau core operation, trong transaction |

### PCF Lifecycle Methods
| Method | Khi nào gọi |
|---|---|
| `init()` | Khởi tạo component lần đầu |
| `updateView()` | Khi data hoặc parameters thay đổi |
| `getOutputs()` | Trước khi framework lấy giá trị output |
| `destroy()` | Khi component bị xóa khỏi DOM |

### Dataverse Web API OData Headers
| Header | Mục đích |
|---|---|
| `Prefer: odata.track-changes` | Bật delta tracking để sync thay đổi |
| `Prefer: odata.maxpagesize=N` | Giới hạn số records mỗi page |
| `Prefer: return=representation` | Trả về entity sau create/update |
| `Prefer: odata.include-annotations=*` | Include formatted values |

### Integration Patterns
| Pattern | Mô tả | Use case |
|---|---|---|
| Webhook | Synchronous, HTTP callback | Cần phản hồi ngay |
| Azure Service Bus | Async, message queue | High-scale, reliable delivery |
| Azure Event Hub | Async, event streaming | Telemetry, high-throughput |
| Azure Event Grid | Event routing | Event-driven architecture |