from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    if not os.path.exists('generated_media'):
        os.makedirs('generated_media')
    app.run(debug=True, host='0.0.0.0', port=5000)
