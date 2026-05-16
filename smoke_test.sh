#!/usr/bin/env bash
set -euo pipefail

BASE_URL=http://localhost:8000
PRODUCT_URL=http://localhost:8001
ORDER_URL=http://localhost:8002

SUFFIX=$(date +%s)
USERNAME="Smoke Test ${SUFFIX}"
EMAIL="smoketest+${SUFFIX}@example.com"
PRODUCT_NAME="Smoke Product ${SUFFIX}"

printf "\nRunning smoke test against local services...\n"

printf "\n1. Create a test user\n"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
  -H "Content-Type: application/json" \
  -d '{"username":"'"$USERNAME"'","email":"'"$EMAIL"'","password":"secret"}')
printf "User response: %s\n" "$USER_RESPONSE"

printf "\n2. Login and get token\n"
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"'"$EMAIL"'","password":"secret"}')
TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data.get("access_token", ""))')
if [ -z "$TOKEN" ]; then
  printf "Failed to obtain token. Response: %s\n" "$TOKEN_RESPONSE"
  exit 1
fi
printf "Token: %s\n" "$TOKEN"

printf "\n3. Create a test product\n"
PRODUCT_RESPONSE=$(curl -s -X POST "$PRODUCT_URL/products/" \
  -H "Content-Type: application/json" \
  -d '{"name":"'"$PRODUCT_NAME"'","price":12.99,"description":"Smoke test product","category":"demo"}')
PRODUCT_ID=$(echo "$PRODUCT_RESPONSE" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data.get("id", ""))')
if [ -z "$PRODUCT_ID" ]; then
  printf "Failed to create product. Response: %s\n" "$PRODUCT_RESPONSE"
  exit 1
fi
printf "Product response: %s\n" "$PRODUCT_RESPONSE"

printf "\n4. Create an order\n"
ORDER_RESPONSE=$(curl -s -X POST "$ORDER_URL/orders/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":'$PRODUCT_ID',"quantity":1}')
ORDER_ID=$(echo "$ORDER_RESPONSE" | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')
printf "Order response: %s\n" "$ORDER_RESPONSE"

printf "\n5. Pay the order\n"
PAID_RESPONSE=$(curl -s -X POST "$ORDER_URL/orders/$ORDER_ID/pay" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"payment_method":"card"}')
printf "Paid response: %s\n" "$PAID_RESPONSE"

printf "\n6. Complete the order\n"
COMPLETED_RESPONSE=$(curl -s -X POST "$ORDER_URL/orders/$ORDER_ID/complete" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" )
printf "Completed response: %s\n" "$COMPLETED_RESPONSE"

printf "\n7. Verify user order history\n"
HISTORY_RESPONSE=$(curl -s "$ORDER_URL/me/orders" \
  -H "Authorization: Bearer $TOKEN")
printf "Order history response: %s\n" "$HISTORY_RESPONSE"

printf "\nSmoke test completed successfully.\n"
