mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"qiu117164@gapps.uwcsea.edu.sg\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
