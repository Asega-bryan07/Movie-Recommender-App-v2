# streamlit run c:\Users\HERLAB26\Documents\Desktop\movie-rec-app\app.py -- for local host

mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml