import streamlit as st
import requests
import time
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import numpy as np

# Initialize session state for metrics history
if 'metrics_history' not in st.session_state:
    st.session_state.metrics_history = []

st.title('ViT Image Classification')

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    if st.button('Classify'):
        # Prepare the file for upload
        files = {'file': ('image.jpg', uploaded_file, 'image/jpeg')}
        
        try:
            # Make prediction request
            start_time = time.time()
            response = requests.post('http://127.0.0.1:8000/predict', files=files)
            response.raise_for_status()
            
            result = response.json()
            
            # Display results
            st.success(f"Predicted Class: {result['class']}")
            st.info(f"Confidence: {result['confidence']:.2%}")
            st.info(f"Inference Time: {result['inference_time']:.3f} seconds")
            
            # Get metrics
            metrics_response = requests.get('http://127.0.0.1:8000/metrics')
            metrics = metrics_response.json()
            
            # Add to metrics history
            st.session_state.metrics_history.append({
                'timestamp': time.time(),
                'inference_time': result['inference_time'],
                'total_requests': metrics['total_requests'],
                'successful_requests': metrics['successful_requests']
            })
            
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")

# Metrics Dashboard
st.header('Model Performance Metrics')

if st.session_state.metrics_history:
    # Convert metrics history to DataFrame
    df = pd.DataFrame(st.session_state.metrics_history)
    
    # Latency over time
    fig_latency = go.Figure()
    fig_latency.add_trace(go.Scatter(
        x=df.index,
        y=df['inference_time'],
        mode='lines+markers',
        name='Inference Time'
    ))
    fig_latency.update_layout(title='Latency Over Time', 
                            xaxis_title='Request Number',
                            yaxis_title='Inference Time (s)')
    st.plotly_chart(fig_latency)
    
    # Throughput (requests per minute)
    window_size = 60  # 1 minute
    timestamps = df['timestamp'].values
    request_counts = np.zeros_like(timestamps)
    for i in range(len(timestamps)):
        window_start = timestamps[i] - window_size
        request_counts[i] = np.sum((timestamps >= window_start) & (timestamps <= timestamps[i]))
    
    fig_throughput = go.Figure()
    fig_throughput.add_trace(go.Scatter(
        x=df.index,
        y=request_counts,
        mode='lines+markers',
        name='Requests per Minute'
    ))
    fig_throughput.update_layout(title='Throughput Over Time',
                               xaxis_title='Request Number',
                               yaxis_title='Requests per Minute')
    st.plotly_chart(fig_throughput)
    
    # Current metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Requests", df['total_requests'].iloc[-1])
    with col2:
        st.metric("Successful Requests", df['successful_requests'].iloc[-1])
    with col3:
        avg_latency = df['inference_time'].mean()
        st.metric("Average Latency", f"{avg_latency:.3f}s")