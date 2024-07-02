import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Function to handle file upload and analysis
def sequence_analysis_page(title, session_key_file, session_key_counts):
    st.title(title)
    
    uploaded_file = st.file_uploader("Upload a file", type=["fastqsanger"], key=session_key_file)
    
    if uploaded_file:
        file_content = uploaded_file.getvalue().decode('utf-8')
        sequences = file_content.splitlines()
        
        sequence_to_search = st.text_input("Enter sequence to search for")
        
        if sequence_to_search:
            search_count = sum(seq.count(sequence_to_search) for seq in sequences)
            st.write(f"Found {search_count} occurrences of the sequence.")
            
            trimmed_sequence = st.text_input("Enter trimmed sequence to analyze")
            
            if trimmed_sequence:
                trimmed_counts = [seq.count(trimmed_sequence) for seq in sequences]
                max_count = max(trimmed_counts)
                normalized_counts = [(seq, count / max_count) for seq, count in zip(sequences, trimmed_counts) if count > 0]
                normalized_counts.sort(key=lambda x: x[1], reverse=True)
                
                st.session_state[session_key_counts] = normalized_counts
                
                # Display normalized counts
                sorted_counts_text = "\n".join([f"{count:.4f} {seq}" for seq, count in normalized_counts])
                st.text_area("Sorted Unique Sequences by Frequency", value=sorted_counts_text, height=300)
                
                # Download button
                sorted_counts_io = io.StringIO(sorted_counts_text)
                st.download_button(
                    label="Download Sorted Unique Sequences by Frequency",
                    data=sorted_counts_io.getvalue(),
                    file_name="sorted_unique_sequences.txt",
                    mime="text/plain"
                )
                
                # Plotting
                ranks = list(range(1, len(normalized_counts) + 1))
                normalized_values = [count for seq, count in normalized_counts]
                plt.figure(figsize=(10, 6))
                plt.scatter(ranks, normalized_values)
                plt.xlabel('Rank')
                plt.ylabel('Normalized Recombination')
                plt.title('Rank vs Normalized Recombination')
                plt.grid(True)
                st.pyplot(plt)

    return st.session_state.get(session_key_counts, None)

# Function to compare sequences from multiple files
def comparison_page(file1_counts, file2_counts, file3_counts):
    st.title("Comparison of Sequences")
    
    if file1_counts and file2_counts and file3_counts:
        combined_counts = {}
        
        for seq, count in file1_counts:
            if seq not in combined_counts:
                combined_counts[seq] = []
            combined_counts[seq].append(count)
        
        for seq, count in file2_counts:
            if seq not in combined_counts:
                combined_counts[seq] = []
            combined_counts[seq].append(count)
        
        for seq, count in file3_counts:
            if seq not in combined_counts:
                combined_counts[seq] = []
            combined_counts[seq].append(count)
        
        average_counts = [(seq, sum(counts) / len(counts)) for seq, counts in combined_counts.items()]
        average_counts.sort(key=lambda x: x[1], reverse=True)
        
        # Display average counts
        sorted_counts_text = "\n".join([f"{count:.4f} {seq}" for seq, count in average_counts])
        st.text_area("Average Normalized Counts", value=sorted_counts_text, height=300)
        
        # Plotting
        ranks = list(range(1, len(average_counts) + 1))
        avg_normalized_values = [count for seq, count in average_counts]
        
        plt.figure(figsize=(10, 6))
        plt.scatter(ranks, avg_normalized_values, label='Average', color='black')

        for seq, count in file1_counts:
            plt.scatter(ranks, [c for s, c in average_counts if s == seq], label='File 1', color='red')
        
        for seq, count in file2_counts:
            plt.scatter(ranks, [c for s, c in average_counts if s == seq], label='File 2', color='green')
        
        for seq, count in file3_counts:
            plt.scatter(ranks, [c for s, c in average_counts if s == seq], label='File 3', color='blue')

        plt.xlabel('Rank')
        plt.ylabel('Normalized Recombination')
        plt.title('Rank vs Normalized Recombination Across Files')
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

# Define the pages
st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["File 1 Analysis", "File 2 Analysis", "File 3 Analysis", "Comparison"])

# Initialize session state
if 'file1_counts' not in st.session_state:
    st.session_state['file1_counts'] = None
if 'file2_counts' not in st.session_state:
    st.session_state['file2_counts'] = None
if 'file3_counts' not in st.session_state:
    st.session_state['file3_counts'] = None

# Page navigation
if page == "File 1 Analysis":
    st.session_state.file1_counts = sequence_analysis_page("File 1 Analysis", "file1", "file1_counts")
elif page == "File 2 Analysis":
    st.session_state.file2_counts = sequence_analysis_page("File 2 Analysis", "file2", "file2_counts")
elif page == "File 3 Analysis":
    st.session_state.file3_counts = sequence_analysis_page("File 3 Analysis", "file3", "file3_counts")
elif page == "Comparison":
    comparison_page(st.session_state.file1_counts, st.session_state.file2_counts, st.session_state.file3_counts)
