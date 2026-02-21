from app import criar_app

app = criar_app()

if __name__ == '__main__':
    # Roda o servidor na porta 5000 
    app.run(debug=True)