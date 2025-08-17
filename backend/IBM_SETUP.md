# IBM watsonx.ai Integration Setup

## Quick Start

### 1. Get IBM Cloud Credentials

1. **Create IBM Cloud Account**: https://cloud.ibm.com/registration
2. **Create watsonx.ai Project**:
   - Go to https://dataplatform.cloud.ibm.com/wx/home
   - Create a new project
   - Copy the **Project ID** from project settings

3. **Generate API Key**:
   - Go to https://cloud.ibm.com/iam/apikeys
   - Click "Create an IBM Cloud API key"
   - Copy the API key

### 2. Configure Environment Variables

Add these to your `.env` file:

```bash
# Switch to IBM watsonx.ai
LLM_PROVIDER=watsonx

# IBM watsonx.ai Configuration
WATSONX_API_KEY=your_ibm_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_REGION=us-south  # or eu-de, eu-gb, jp-tok
WATSONX_API_VERSION=2025-02-11
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Keep your existing MCP configuration
MCP_BASE_URL=http://localhost:8080
```

### 3. Test the Integration

```bash
# Start the application
uvicorn main:app --reload

# Test the API
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=8888888888" \
  -d '{"prompt": "What is my spending this month?"}'
```

## Available Models

You can change `WATSONX_MODEL_ID` to any of these:

- `ibm/granite-3-8b-instruct` (default, balanced)
- `ibm/granite-3-2b-instruct` (faster, lighter)
- `meta-llama/llama-3-1-70b-instruct` (more capable)
- `mistralai/mistral-large` (high quality)
- `meta-llama/llama-3-2-90b-vision-instruct` (multimodal)

## Switching Between Providers

To switch back to Google:
```bash
LLM_PROVIDER=google
```

To use IBM watsonx.ai:
```bash
LLM_PROVIDER=watsonx
```

## Features That Work Identically

✅ All financial queries and analysis
✅ Smart context-aware responses  
✅ Streaming responses (SSE)
✅ Chat history and sessions
✅ Goal management
✅ Transaction analysis
✅ Celebrity comparisons (still uses Gemini)
✅ MCP server integration

## Troubleshooting

### Invalid API Key
- Verify your API key at https://cloud.ibm.com/iam/apikeys
- Ensure no extra spaces in the `.env` file

### Project ID Not Found
- Check project ID at https://dataplatform.cloud.ibm.com/projects
- Must be the full UUID (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

### Region Issues
- Available regions: `us-south`, `eu-de`, `eu-gb`, `jp-tok`
- Default is `us-south` (most reliable)

### Model Not Available
- Some models require specific regions
- Start with `ibm/granite-3-8b-instruct` for testing

## No Code Changes Required! 🎉

The integration is completely drop-in. Your existing code remains unchanged:
- Same API endpoints
- Same response formats
- Same Flutter UI compatibility
- Just different AI provider under the hood
