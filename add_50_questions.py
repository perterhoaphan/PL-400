import docx
import json
import re

# Read the Word document
doc = docx.Document('Question 50.docx')
full_text = '\n'.join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

# Read existing questions
with open('questions.json', 'r', encoding='utf-8') as f:
    existing_questions = json.load(f)

current_max_id = max(q['id'] for q in existing_questions)
print(f"Current max ID: {current_max_id}, Total existing: {len(existing_questions)}")

# Split into individual questions using "Question X of 50" pattern
# The first question may not have the header
parts = re.split(r'Question \d+ of 50', full_text)

# Parse each question
new_questions = []

# Map categories based on question content/topic
def categorize_question(question_text, options):
    """Categorize based on question content keywords."""
    text = (question_text + ' '.join(options)).lower()
    
    if any(kw in text for kw in ['plug-in', 'plugin', 'webhook', 'service bus', 'event hub', 'event grid', 
                                   'azure function', 'custom api', 'service endpoint', 'assembly',
                                   'prevalidation', 'preoperation', 'postoperation', 'execution context',
                                   'executetransaction', 'upsert', 'timeout error', 'asynchronously']):
        return "Extend the Platform"
    elif any(kw in text for kw in ['pcf', 'pac ', 'msbuild', 'solution checker', 'managed solution',
                                     'alm', 'solution layer', 'deployment', 'pipeline', 'unmanaged',
                                     'pac pcf', 'pac auth', 'pac solution', 'cdsproj', 'dotnet',
                                     'notifyoutputchanged', 'component framework']):
        return "Build Solutions"
    elif any(kw in text for kw in ['canvas app', 'power apps monitor', 'powerfx', 'drop-down',
                                     'items property', 'onselect', 'preload', 'teams', 'trace',
                                     'log', 'monitor']):
        return "Power Apps"
    elif any(kw in text for kw in ['command bar', 'ribbon', 'form event', 'onsave', 'onload',
                                     'client script', 'web resource', 'formcontext', 'business rule',
                                     'show or hide', 'visibility', 'form properties', 'split button',
                                     'command designer', 'ribbon workbench', 'quick actions']):
        return "User Experience"
    elif any(kw in text for kw in ['power automate', 'cloud flow', 'connector', 'custom connector',
                                     'oauth', 'cors', 'web api', 'odata', 'fetchxml', 'api key',
                                     'trigger condition', 'configure run after', 'skip token',
                                     'pagination', 'list rows', 'http trigger', 'swagger',
                                     'chunking', 'graph api', 'key vault', 'service principal',
                                     'entra id', 'azure ad']):
        return "Integrations"
    elif any(kw in text for kw in ['business rule', 'client scripting', 'synchronous', 'asynchronous',
                                     'authentication', 'client secret', 'basic auth', 'dual-write',
                                     'virtual table', 'lookup', 'javascript', '_value']):
        return "Technical Design"
    else:
        return "Technical Design"  # Default


def parse_question_block(block):
    """Parse a single question block into structured format."""
    lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
    if not lines:
        return None
    
    # Find the question text, selection instruction, and options
    question_lines = []
    options = []
    selection_type = 'single'
    reading_question = True
    reading_options = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for selection instruction
        if line.startswith('Select only one answer') or line.startswith('Select all answers that apply'):
            if 'all answers' in line:
                selection_type = 'multi'
            reading_question = False
            reading_options = True
            i += 1
            continue
        
        # Check for "Choose two" or "Choose three" in the question
        if 'select two' in line.lower() or 'choose two' in line.lower():
            selection_type = 'multi'
        elif 'select three' in line.lower() or 'choose three' in line.lower():
            selection_type = 'multi'
        elif 'select all' in line.lower():
            selection_type = 'multi'
        
        if reading_question and not reading_options:
            # Skip lines that are just selection instructions
            if not line.startswith('Select '):
                question_lines.append(line)
        elif reading_options:
            # Options are non-empty lines after selection instruction
            if line and not line.startswith('Select '):
                options.append(line)
        
        i += 1
    
    if not question_lines or not options:
        return None
    
    question_text = ' '.join(question_lines)
    
    return {
        'question': question_text,
        'options': options,
        'type': selection_type
    }


# Manually define the 50 questions with correct answers based on the document content
# This is needed because the docx doesn't have answer markers
questions_data = [
    {
        "question": "You need to display data from a Microsoft SQL database in a model-driven Power Apps form. The data must always be current. You must minimize the amount of data storage used. Which feature should you use?",
        "options": ["Dual-write", "Virtual tables", "Connectors", "Activity tables"],
        "correct": [1],
        "type": "single",
        "category": "Technical Design",
        "explanation": "Virtual tables display data from external sources like SQL without storing data in Dataverse, keeping data current and minimizing storage."
    },
    {
        "question": "You have a model-driven app. You are customizing the main form for a Microsoft Dataverse table. Users must enter a value in a column named VPApprover when the value in a column named Revenue is greater than one million. You need to implement the logic. What should you use?",
        "options": ["Cloud flow", "Business process flow", "Workflow", "Business rule"],
        "correct": [3],
        "type": "single",
        "category": "Technical Design",
        "explanation": "Business rules can enforce field requirements based on conditions directly on model-driven app forms without code."
    },
    {
        "question": "You are creating business logic that performs operations on data in Dataverse. You need to ensure the business logic is performed as part of a Dataverse transaction. Which two actions should you perform?",
        "options": ["Build a Dataverse plug-in.", "Create a Power Automate cloud flow.", "Register a webhook for an Azure function.", "Register a service endpoint for Azure Service Bus."],
        "correct": [0],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "Only Dataverse plug-ins execute within the Dataverse transaction pipeline. Cloud flows, webhooks, and service endpoints are external and asynchronous."
    },
    {
        "question": "You are developing a model-driven app. The app must run specific code when a user selects a button on the ribbon. You need to ensure that only specific users can run the code. What should you use?",
        "options": ["Custom API", "Custom process action", "Classic workflow", "Business rule"],
        "correct": [0],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "Custom API allows you to create actions that can be secured with privilege checks, ensuring only users with specific security roles can execute the code."
    },
    {
        "question": "You are developing a canvas app. You need to implement a custom visual in the app. Which approach should you use?",
        "options": ["Client scripting", "Power Apps component framework code component", "Web API", "Liquid template"],
        "correct": [1],
        "type": "single",
        "category": "Build Solutions",
        "explanation": "Power Apps component framework (PCF) code components are the supported way to create custom visuals for canvas apps."
    },
    {
        "question": "A company has an internal system with a SOAP API. You need to create an integration between the system and Microsoft Dataverse. Which three integration options should you use?",
        "options": ["Azure function", "Custom connector", "Custom API", "HTTP request", "Business rule"],
        "correct": [0, 1, 3],
        "type": "multi",
        "category": "Integrations",
        "explanation": "Azure functions, custom connectors, and HTTP requests can handle SOAP API integration. Business rules and Custom API cannot directly integrate with SOAP services."
    },
    {
        "question": "You are developing a plug-in that integrates with Microsoft Dataverse. You need to pass secured configuration data to the class constructor while registering the plug-in. Where is the secured configuration data stored?",
        "options": ["Table", "JSON file", "Config file", "XML file"],
        "correct": [0],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "Secured configuration data for plug-ins is stored in the SdkMessageProcessingStepSecureConfig table in Dataverse, accessible only to System Administrators."
    },
    {
        "question": "You develop a plug-in. You need to test the plug-in in a development environment. What should you register first to run the plug-in?",
        "options": ["step", "image", "assembly", "service endpoint"],
        "correct": [2],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "You must register the assembly first using the Plug-in Registration Tool before you can register steps and images."
    },
    {
        "question": "A company has a Dataverse custom API message in Power Apps. You need to build business logic for the custom API and configure the custom API to run the business logic. Which three actions should you perform?",
        "options": ["Write a workflow extension.", "Write a plug-in for the custom API.", "Register a step by using the Plug-in Registration tool (PRT).", "Update the custom API plug-in type in Power Apps.", "Register the assembly using the Plug-in Registration tool (PRT).", "Define an entity image using the Plug-in Registration tool (PRT)."],
        "correct": [1, 4, 3],
        "type": "multi",
        "category": "Extend the Platform",
        "explanation": "You need to write a plug-in, register the assembly using PRT, and then update the custom API plug-in type in Power Apps to link the plug-in to the custom API."
    },
    {
        "question": "A company builds a custom API bound to a Microsoft Dataverse table. The company requires a Power Automate cloud flow that is triggered when the custom API is called. You need to configure the custom API. Which two actions should you perform?",
        "options": ["Register a step.", "Create a catalog.", "Create a category.", "Create the custom API as a function.", "Extend the BusinessEventContract class."],
        "correct": [0, 1],
        "type": "multi",
        "category": "Extend the Platform",
        "explanation": "To trigger a cloud flow from a custom API, you need to register a step and create a catalog to make it available as a business event."
    },
    {
        "question": "A company has a plug-in that runs asynchronously in the PostOperation stage of a table update. The plug-in causes a timeout error. You need to improve the performance of the plug-in. What should you do?",
        "options": ["Define entity images.", "Implement retry logic.", "Enable Application Insights.", "Change the execution mode to synchronous."],
        "correct": [0],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "Defining entity images reduces the number of queries the plug-in needs to make to retrieve entity data, improving performance and reducing timeout risk."
    },
    {
        "question": "A company uses Microsoft Power Platform. The Power Platform makers want to use data from a web app in canvas apps. The web app has an API secured by a Microsoft personal account. You need to configure authentication for a custom connector. Which two connection parameters should you configure?",
        "options": ["client ID", "username", "client secret", "authorization URL", "parameter location"],
        "correct": [0, 2],
        "type": "multi",
        "category": "Integrations",
        "explanation": "For OAuth 2.0 authentication with Microsoft personal accounts, you need to configure client ID and client secret as connection parameters."
    },
    {
        "question": "A company uses Microsoft Power Platform. The Power Platform makers want to perform complex calculations in canvas apps. You build an Azure function to perform the calculations. You need to configure the Azure function and the authentication for the custom connector. Which three actions should you perform?",
        "options": ["Use Get function URL.", "Configure the Azure function with a HTTP trigger.", "Configure the Azure function with a queue trigger.", "Register an application in Microsoft Entra ID.", "Select API key for authentication type in the custom connector.", "Select OAuth 2.0 for authentication type in the custom connector."],
        "correct": [0, 1, 4],
        "type": "multi",
        "category": "Integrations",
        "explanation": "You need to configure HTTP trigger for the Azure function, get its URL, and use API key authentication in the custom connector."
    },
    {
        "question": "You build a custom connector for an API that supports large messages with chunking. You need to enable the custom connector to support chunking. What should you do?",
        "options": ["Import the API into Azure API Management.", "Run the pac connector update command for Microsoft Power Platform CLI.", "Edit the connector's swagger file in the Swagger editor and add x-ms-capabilities.", "Run the paconn validate --api-def command for Microsoft Power Platform Connectors CLI."],
        "correct": [2],
        "type": "single",
        "category": "Integrations",
        "explanation": "To enable chunking support in a custom connector, you need to edit the swagger definition file and add the x-ms-capabilities property."
    },
    {
        "question": "A company has a custom table named TableA that has a lookup field to the contact table (schemaname: pref_ContactId, logicalname: pref_contactid), related to another custom table named TableB. You are developing an onLoad JavaScript function for TableB using web API and OData. You need to check the response from web API. Which attribute should you check?",
        "options": ["pref_ContactId", "pref_contactid", "_pref_ContactId_value", "_pref_contactid_value"],
        "correct": [3],
        "type": "single",
        "category": "Integrations",
        "explanation": "When using Web API/OData, lookup fields are returned with underscore prefix, logical name (lowercase), and _value suffix: _pref_contactid_value."
    },
    {
        "question": "You are a developer for a Microsoft Power Platform implementation. You require JavaScript to make requests to the web API. You need to recommend an option to query data. Which two options should you recommend?",
        "options": ["FetchXML", "OData v2.0", "OData v4.0", "QueryExpression"],
        "correct": [0, 2],
        "type": "multi",
        "category": "Integrations",
        "explanation": "The Dataverse Web API supports FetchXML and OData v4.0 for querying data. OData v2.0 and QueryExpression are not supported by the Web API."
    },
    {
        "question": "A company plans to use Microsoft Power Platform. You need to write a JavaScript method that shows a message when a record has been created by impersonation. Which field should you use?",
        "options": ["ownerid", "createdby", "modifiedby", "createdonbehalfby"],
        "correct": [3],
        "type": "single",
        "category": "Technical Design",
        "explanation": "The createdonbehalfby field identifies the delegate user who created the record on behalf of another user (impersonation)."
    },
    {
        "question": "You use the Organization service to process data in Microsoft Dataverse tables. You have a regular process that updates thousands of rows on the Contact table from an external system. You need to use a method that has the highest throughput and will roll back all updates if any error occurs. Which method should you use?",
        "options": ["UpdateMultiple", "ExecuteAsyncRequest", "ExecuteMultipleRequest", "ExecuteTransactionRequest"],
        "correct": [3],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "ExecuteTransactionRequest executes all operations in a single transaction and rolls back all changes if any operation fails."
    },
    {
        "question": "An organization uses Power Apps to track permits for new buildings. You must create a durable timer in the orchestrator function. What should you call?",
        "options": ["setTimeout() function", "setInterval() function", "Task.Delay() method", "createTimer() method"],
        "correct": [3],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "In Azure Durable Functions, the createTimer() method is used to create durable timers in the orchestrator function."
    },
    {
        "question": "You develop a plug-in that creates and relates many records when a specific event occurs. During user acceptance testing, the plug-in generates timeout errors. You need to resolve the issue. What should you do?",
        "options": ["Configure the plug-in to run asynchronously.", "Create an Azure Function that performs processing and call the function from the plug-in.", "Create several threads in the plug-in.", "Split the plug-in into two plug-ins that both run for the event."],
        "correct": [0],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "Configuring the plug-in to run asynchronously removes the 2-minute timeout limit and allows long-running operations to complete."
    },
    {
        "question": "A company uses Microsoft Power Platform. The company plans to use Azure Functions to perform process-heavy calculations. You need to identify the maximum time-out duration for a consumption plan. Which time-out duration should you identify?",
        "options": ["2 minutes", "5 minutes", "10 minutes", "Unlimited"],
        "correct": [2],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "The default timeout for Azure Functions Consumption plan is 5 minutes, but can be configured up to a maximum of 10 minutes."
    },
    {
        "question": "You have a Power Automate cloud flow. The flow has an action that calls an external API. You need to ensure that an immediate notification is sent if an error occurs in the action. Which two actions should you perform?",
        "options": ["Add an email notification action to the main branch of the flow.", "Set the value of the Configure run after setting for the email notification step to is successful.", "Add a parallel branch that contains an email notification action to the flow.", "Set the value of the Configure run after setting for the email notification action to has failed."],
        "correct": [2, 3],
        "type": "multi",
        "category": "Integrations",
        "explanation": "Add a parallel branch with an email notification and configure its 'run after' setting to 'has failed' to send notification on error."
    },
    {
        "question": "You have a Power Automate flow. The flow must run whenever a user adds a document to a SharePoint list and a column in a list named Status has a value. Which two expressions can you use in a trigger condition?",
        "options": ["@not(empty(triggerBody()?['Status']))", "@(empty(triggerBody()?['Status'])", "@not(equals(triggerBody()?['Status'],null))", "@(equals(triggerBody()?['Status'],null)"],
        "correct": [0, 2],
        "type": "multi",
        "category": "Integrations",
        "explanation": "Both @not(empty(...)) and @not(equals(...,null)) check that the Status field has a value. The other options check for empty/null without negation."
    },
    {
        "question": "You create a Power Automate flow that gets data from Dataverse by using the List rows action. The result may contain more than 100,000 rows. You need to ensure the flow can handle all the results. Which three actions should you perform?",
        "options": ["Add a new string variable to store the skip token.", "Activate pagination on the List rows action.", "Create a do-while loop for as long as the skip token variable is not empty. Add the list row to the loop and use the stored skip token.", "Add a new Boolean variable to store more records.", "Fetch the skip token from the List rows action and store it in another variable."],
        "correct": [0, 2, 4],
        "type": "multi",
        "category": "Integrations",
        "explanation": "For large datasets exceeding pagination limits, use skip tokens: store the skip token in a variable, create a do-while loop, and fetch/store the skip token from each List rows result."
    },
    {
        "question": "You are building a Power Automate cloud flow that is triggered when a Dataverse table row is updated. You need to configure the trigger so the flow only runs when a row is deactivated. Which two properties should you configure?",
        "options": ["Scope", "Row filter", "Row count", "Column filter", "FetchXML query"],
        "correct": [1, 3],
        "type": "multi",
        "category": "Integrations",
        "explanation": "Use Column filter to specify the statecode column, and Row filter to filter for the inactive state value to trigger only on deactivation."
    },
    {
        "question": "You are creating a cloud flow. You need to ensure that the flow action runs without a user account and accesses the Graph API without requiring credentials to be specified in the flow. Which three steps should you perform?",
        "options": ["Create a service principal in Microsoft Entra ID.", "Create a custom security role in Microsoft Dataverse.", "Store the service principal credentials inside Azure Key Vault.", "Configure License to role mapping in the Dataverse environment settings.", "Assign the service principal to an application user in the Microsoft Dataverse environment.", "Configure Hierarchy security in the Dataverse environment settings."],
        "correct": [0, 2, 4],
        "type": "multi",
        "category": "Integrations",
        "explanation": "Create a service principal in Entra ID, store credentials in Azure Key Vault for security, and assign the service principal to an application user in Dataverse."
    },
    {
        "question": "You have an automated cloud flow that connects to a Microsoft Dataverse table named Cruises (schema: Cr8ec_cruises). You need to ensure that the flow runs only for rows with destination Cozumel and boat name Oasis. Which trigger condition should you use?",
        "options": [
            "@and(equals(triggerOutputs()?['cr8ec_destination'], 'Cozumel'), equals(triggerOutputs()?['cr8ec_boatname'],'Oasis'))",
            "@and(equals(triggerOutputs()?['_cr8ec_destination_label'], 'Cozumel'), equals(triggerOutputs()?['_cr8ec_boatname_label'],'Oasis'))",
            "@and(equals(triggerBody()?['cr8ec_destination'], 'Cozumel'), equals(triggerBody()?['cr8ec_boatname'],'Oasis'))",
            "@and(equals(triggerBody()?['_cr8ec_destination_label'], 'Cozumel'), equals(triggerBody()?['_cr8ec_boatname_label'],'Oasis'))"
        ],
        "correct": [0],
        "type": "single",
        "category": "Integrations",
        "explanation": "For choice columns in trigger conditions, use triggerOutputs() with the schema name directly to compare choice values."
    },
    {
        "question": "You develop a solution to integrate Dynamics 365 Customer Engagement (on-premises) data with custom code hosted on external services. You need to ensure that if any failure happens during the execution, the failure is reported to the app user immediately. What should you do?",
        "options": ["Use Azure Service Bus and set the execution mode to synchronous.", "Use webhooks and set the execution mode to synchronous.", "Use webhooks and set the execution mode to asynchronous.", "Use Azure Service Bus and enable the auto-forwarding feature."],
        "correct": [1],
        "type": "single",
        "category": "Integrations",
        "explanation": "Webhooks with synchronous execution mode will report failures immediately to the user. Asynchronous mode would not provide immediate feedback."
    },
    {
        "question": "You manage a Microsoft Dataverse instance. You need to use synchronous processing to publish events from the Microsoft Dataverse instance to an external service. What should you use?",
        "options": ["Azure Service Bus", "Webhook", "Azure Event Grid", "Azure Event Hub"],
        "correct": [1],
        "type": "single",
        "category": "Integrations",
        "explanation": "Webhooks support synchronous processing for publishing Dataverse events to external services. Azure Service Bus, Event Grid, and Event Hub are asynchronous."
    },
    {
        "question": "You are registering a webhook to publish Microsoft Dataverse events by using the Plug-in Registration Tool. You need to ensure that the webhook is triggered only when a specific column value is updated. Which two actions should you perform?",
        "options": ["Register a new step.", "Register a new image.", "Configure Filtering Attributes.", "Configure the execution stage.", "Configure Pre Image and Post Image."],
        "correct": [0, 2],
        "type": "multi",
        "category": "Extend the Platform",
        "explanation": "Register a new step for the webhook and configure Filtering Attributes to specify which column changes should trigger the webhook."
    },
    {
        "question": "An organization uses Microsoft Dataverse. You need to synchronize data from an external system. If a record exists, update it; if not, create a new record. Which operation should you use?",
        "options": ["Create", "Update", "Upsert", "SetState"],
        "correct": [2],
        "type": "single",
        "category": "Extend the Platform",
        "explanation": "Upsert (Update + Insert) checks if the record exists and updates it, or creates a new record if it doesn't exist."
    },
    {
        "question": "You are configuring a Power Apps model-driven app. You create a query to confirm data sync with external systems. The query must return the total number of changed rows with data sorted in descending order. When you run the query, it returns an error. What is the reason for the error?",
        "options": ["The Web API request includes the odata.track-changes header.", "The Web API request includes the $count query parameter.", "The Web API header includes the $orderby query parameter.", "The Web API request includes delta links."],
        "correct": [2],
        "type": "single",
        "category": "Integrations",
        "explanation": "The $orderby query parameter is not supported with change tracking (odata.track-changes). This combination causes an error."
    },
    {
        "question": "You are building integrations from external systems that require authentication to Microsoft Dataverse Web API. You need to configure authentication. Which three steps should you perform?",
        "options": ["Create non-interactive users in Dataverse.", "Create app registrations in Microsoft Entra ID.", "Create application users in Dataverse.", "Create Enterprise applications in Microsoft Entra ID.", "Create and select custom security roles.", "Select the Basic User security role."],
        "correct": [1, 2, 4],
        "type": "multi",
        "category": "Integrations",
        "explanation": "Create app registrations in Entra ID, create application users in Dataverse, and assign custom security roles for proper authentication and authorization."
    },
    {
        "question": "A company uses Microsoft Power Platform. The company plans to use Microsoft Power Platform pipelines to deploy solutions from development to test and production environments by using a separate host environment. You need to configure the environments. Which two environments should you configure?",
        "options": ["default", "development", "host", "production", "test"],
        "correct": [2, 3],
        "type": "multi",
        "category": "Build Solutions",
        "explanation": "You need to configure the host environment (where pipelines run) and production environment as target. Development is the source, not needing special pipeline config."
    },
    {
        "question": "You manage the ALM process. During a solution restructuring, you merge and consolidate several managed solutions. When you attempt to uninstall an old managed solution, you receive a dependency error. You need to remove the dependency. Which three actions should you perform?",
        "options": ["Identify the topmost solution on the dependent component in the target organization.", "Uninstall the solution layer with the dependency from the target environment.", "Export the new version as managed and upgrade the solution in the target environment.", "Export the new version as unmanaged and update the solution in the target environment.", "Prepare a new version of the solution in the development environment that removes or updates the dependency."],
        "correct": [0, 2, 4],
        "type": "multi",
        "category": "Build Solutions",
        "explanation": "Identify the dependent component, prepare a new version removing the dependency in dev, then export as managed and upgrade in target environment."
    },
    {
        "question": "You plan to delete a table in a Microsoft Power Platform solution. You need to determine whether components are affected by the table deletion. Which two types of components should you inspect?",
        "options": ["Microsoft Word template", "Microsoft Power Automate cloud flow", "Plug-in step for an assembly", "Web resource used in a form"],
        "correct": [1, 2],
        "type": "multi",
        "category": "Build Solutions",
        "explanation": "Power Automate cloud flows and plug-in steps directly reference tables and would be affected by table deletion."
    },
    {
        "question": "You are assisting with the automation of ALM by using Azure DevOps pipelines. You need to pre-populate an environment variable with specific details for the target environments. What should you do?",
        "options": ["Run the Microsoft Power Platform Checker.", "Generate a deployment settings file.", "Add a reference by using the Power Apps CLI.", "Remove the current value before exporting the solution."],
        "correct": [1],
        "type": "single",
        "category": "Build Solutions",
        "explanation": "A deployment settings file allows you to pre-populate environment variables with environment-specific values during automated deployments."
    },
    {
        "question": "A company uses managed solutions. A developer installs Solution1 (PublisherA), Solution2 (PublisherB), Solution3 (PublisherA) into production, all with changes to Account table. The developer edits the account form directly in production. After importing new Solution3, users report form changes are not displayed. What should you delete?",
        "options": ["Solution1", "Solution2", "Solution3", "Active unmanaged layer"],
        "correct": [3],
        "type": "single",
        "category": "Build Solutions",
        "explanation": "Direct edits in production create an active unmanaged layer that overrides managed solution changes. Deleting the unmanaged layer allows the managed solution changes to take effect."
    },
    {
        "question": "You have a model-driven app. Users must be able to launch a third-party application by selecting a button on the command bar. You need to edit the ribbon to add the button. What are two possible ways to achieve this goal?",
        "options": ["Create JavaScript code.", "Use Ribbon Workbench.", "Use a business rule.", "Customize the command bar using command designer."],
        "correct": [1, 3],
        "type": "multi",
        "category": "User Experience",
        "explanation": "Ribbon Workbench and the modern command designer are both valid ways to customize the command bar and add buttons."
    },
    {
        "question": "You are developing a model-driven app. You need to use the client API to extend the behavior of the app. To which two events can you attach client script in the Form editor?",
        "options": ["OnSave", "PreSearch", "PostSearch", "OnLoad"],
        "correct": [0, 3],
        "type": "multi",
        "category": "User Experience",
        "explanation": "In the Form editor, you can attach client scripts to OnSave and OnLoad form events. PreSearch is configured via code, PostSearch doesn't exist."
    },
    {
        "question": "You are developing event handlers for form events. You need to register the event handlers. Which two options can you use?",
        "options": ["Form properties", "Code", "Business rules", "Cloud flows"],
        "correct": [0, 1],
        "type": "multi",
        "category": "User Experience",
        "explanation": "Event handlers can be registered through Form properties (declarative) or through Code (programmatic using addOnLoad, addOnSave, etc.)."
    },
    {
        "question": "You are developing a Power Apps model-driven app. You need to ensure that when a button is selected, the action from the primary command is executed. Which command type should you implement?",
        "options": ["Quick actions", "Split button", "Dropdown", "Group"],
        "correct": [1],
        "type": "single",
        "category": "User Experience",
        "explanation": "A Split button has a primary action that executes when the main button area is clicked, plus a dropdown for additional options."
    },
    {
        "question": "You create a Power Apps component framework (PCF) component by using Visual Studio Code. You receive 'Missing required tool: MSBuild.exe/dotnet.exe' error when packaging. Which two actions should you perform?",
        "options": ["Add MSBuild.exe/dotnet.exe in the Path environment variable.", "Run the msbuild /t:restore command from within the cdsproj directory.", "Use a Visual Studio Code developer command prompt.", "Run the dotnet build command from within the cdsproj directory."],
        "correct": [0, 2],
        "type": "multi",
        "category": "Build Solutions",
        "explanation": "Either add MSBuild.exe/dotnet.exe to the PATH environment variable, or use a Visual Studio developer command prompt which has these tools pre-configured."
    },
    {
        "question": "You are using Power Apps component framework to create code components for a canvas app. You need to bundle all code component elements into a solution file. Which command should you use to generate a zip file from the solution project?",
        "options": ["msbuild /t:build /restore", "msbuild", "msbuild /p:configuration=Release", "msbuild /t:rebuild"],
        "correct": [0],
        "type": "single",
        "category": "Build Solutions",
        "explanation": "msbuild /t:build /restore builds the solution project and generates the solution zip file, restoring NuGet packages first."
    },
    {
        "question": "You are developing an interactive new code component by using the Power Apps component framework. You need to ensure that the output value provided in a textbox is updated in other components. Which two actions should you perform?",
        "options": ["Create an event handler for the textbox for its change event.", "Create an event handler for the other components for its change event.", "Invoke the notifyOutputChanged method from the init method.", "Invoke the updateView method from the event handler.", "Invoke the notifyOutputChanged method from the event handler.", "Invoke the notifyOutputChanged method from the updateView method."],
        "correct": [0, 4],
        "type": "multi",
        "category": "Build Solutions",
        "explanation": "Create a change event handler for the textbox and invoke notifyOutputChanged from that event handler to notify the framework that output has changed."
    },
    {
        "question": "You develop a canvas app to manage time off requests. The Request table has a lookup to AbsenceType. You need to ensure users only select active absence types from a drop-down list. What should you do?",
        "options": [
            "Add Filter('Absence Types', 'Absence Types (Views)'.'Active Absence Types') to the onSelect property",
            "Add 'Absence Types' to the onSelect property",
            "Add Filter('Absence Types', 'Absence Types (Views)'.'Active Absence Types') to the Items property",
            "Add 'Absence Types' to the Items property"
        ],
        "correct": [2],
        "type": "single",
        "category": "Power Apps",
        "explanation": "Use the Items property (not onSelect) with a Filter expression to show only active absence types from the Dataverse view."
    },
    {
        "question": "You develop a cloud flow named Get Customers. You add the flow to a canvas app. You need to pass two values from the app to the flow. Which three steps should you perform?",
        "options": ["Use the Manually trigger a flow trigger.", "Use the When Power Apps calls a flow (V2) trigger.", "Configure trigger conditions in the trigger.", "Create two parameters in the trigger.", "Create two variables in the flow.", "Use GetCustomers.Run in the canvas app."],
        "correct": [1, 3, 5],
        "type": "multi",
        "category": "Power Apps",
        "explanation": "Use the 'When Power Apps calls a flow (V2)' trigger, create two parameters in the trigger for the values, and call GetCustomers.Run from the canvas app."
    },
    {
        "question": "You manage a canvas app. You are troubleshooting the app startup performance issue by using Monitor. You need to display a custom message in Monitor. Which function should you use?",
        "options": ["Error", "Notify", "Log", "Trace"],
        "correct": [3],
        "type": "single",
        "category": "Power Apps",
        "explanation": "The Trace function is used to display custom messages in the Monitor tool for debugging and troubleshooting canvas apps."
    },
    {
        "question": "You develop a model-driven app. You need to diagnose and troubleshoot an issue by using Monitor. Which two type of events can you monitor?",
        "options": ["Screen load metrics", "Network", "Page navigation", "User actions"],
        "correct": [1, 2],
        "type": "multi",
        "category": "Power Apps",
        "explanation": "Monitor for model-driven apps can track Network calls and Page navigation events. Screen load metrics and user actions are not directly monitored."
    },
    {
        "question": "You create a form for a model-driven app and add a control. You enable the control but users report it is disabled. You need to identify the root cause using Monitor. What should you do?",
        "options": ["Open the FormControls operation and check the value of the DisableFormControl property.", "Open the ControlStateChange.hidden operation and review the last logged operation.", "Open the ControlStateChange.disabled operation and review the last logged operation.", "Open the FormControls operation and check the value of the Disabled property."],
        "correct": [2],
        "type": "single",
        "category": "Power Apps",
        "explanation": "The ControlStateChange.disabled operation in Monitor shows what caused the control to become disabled, including the last operation that changed its state."
    }
]

# Load existing questions and find max ID
with open('questions.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

max_id = max(q['id'] for q in existing)
print(f"Current max ID: {max_id}")
print(f"Total existing questions: {len(existing)}")

# Add IDs to new questions
for i, q in enumerate(questions_data):
    q['id'] = max_id + 1 + i

# Append new questions
existing.extend(questions_data)

# Save
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"\nAdded {len(questions_data)} new questions")
print(f"New ID range: {max_id + 1} to {max_id + len(questions_data)}")
print(f"Total questions now: {len(existing)}")

# Print category distribution of new questions
from collections import Counter
cats = Counter(q['category'] for q in questions_data)
print(f"\nNew questions by category:")
for cat, count in sorted(cats.items()):
    print(f"  {cat}: {count}")
