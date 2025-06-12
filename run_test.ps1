echo "First, the script will build the project using docker-compose. Wait..."

docker compose -f docker-compose.yml up -d --build
sleep 1
echo ""
echo "Run a Client instance with multiple (stock) Symbols:"
docker compose -f docker-compose.yml run -T --rm client PLTR AMD AAPL AAL NVDA F
echo "(again) Run a Client instance with multiple (stock) Symbols:"
docker compose -f docker-compose.yml run -T --rm client AVGO ARM NVDA PLAY QCOM TSLA ADBE UBER
echo ""
echo "When you are done, do not forget to stop the Docker containers with the following command:"
docker compose -f docker-compose.yml down
echo "Done!"