from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import json
from datetime import datetime
import os

app = Flask(__name__)

# In-memory storage
electricity_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        print("Received data:", request.get_json())  # Debug print
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})
            
        customer_id = data.get('customer_id', '').strip()
        month = data.get('month', '').strip()
        tokens_str = data.get('tokens', '').strip()
        
        if not customer_id or not month or not tokens_str:
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        try:
            tokens = float(tokens_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'Tokens must be a number'})
        
        if customer_id not in electricity_data:
            electricity_data[customer_id] = {}
        
        electricity_data[customer_id][month] = tokens
        
        print(f"Stored data: {electricity_data}")  # Debug print
        
        return jsonify({
            'success': True, 
            'message': f'Data added successfully for {customer_id} - {month}: {tokens} tokens'
        })
    except Exception as e:
        print(f"Error: {e}")  # Debug print
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_averages')
def get_averages():
    try:
        customer_id = request.args.get('customer_id', '').strip()
        print(f"Looking for customer: {customer_id}")  # Debug print
        print(f"Current data: {electricity_data}")  # Debug print
        
        if not customer_id:
            return jsonify({'success': False, 'message': 'Customer ID is required'})
        
        if customer_id not in electricity_data or not electricity_data[customer_id]:
            return jsonify({'success': False, 'message': f'No data found for customer {customer_id}'})
        
        customer_data = electricity_data[customer_id]
        average_tokens = sum(customer_data.values()) / len(customer_data)
        
        return jsonify({
            'success': True,
            'average': round(average_tokens, 2),
            'total_months': len(customer_data),
            'data': customer_data
        })
    except Exception as e:
        print(f"Error in get_averages: {e}")  # Debug print
        return jsonify({'success': False, 'message': str(e)})

@app.route('/generate_chart')
def generate_chart():
    try:
        customer_id = request.args.get('customer_id', '').strip()
        
        if not customer_id:
            return jsonify({'success': False, 'message': 'Customer ID is required'})
        
        if customer_id not in electricity_data or not electricity_data[customer_id]:
            return jsonify({'success': False, 'message': f'No data found for customer {customer_id}'})
        
        customer_data = electricity_data[customer_id]
        
        # Sort months chronologically
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        months = sorted(customer_data.keys(), key=lambda x: month_order.index(x) if x in month_order else 999)
        tokens = [customer_data[month] for month in months]
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(months, tokens, color='skyblue', edgecolor='black')
        plt.xlabel('Months')
        plt.ylabel('Token Consumption')
        plt.title(f'Electricity Token Consumption - Customer {customer_id}')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, token in zip(bars, tokens):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{token}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{plot_url}'
        })
    except Exception as e:
        print(f"Error in generate_chart: {e}")  # Debug print
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_all_customers')
def get_all_customers():
    """Debug endpoint to see all stored data"""
    return jsonify({
        'success': True,
        'customers': list(electricity_data.keys()),
        'all_data': electricity_data
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)