import streamlit as st
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import psutil

# Function to log memory usage
def log_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    st.write(f"Memory Usage: {memory_info.rss / (1024 * 1024)} MB")

st.write("Max upload size:", st.config.get_option("server.maxUploadSize"))

def reverse_complement_sequence(sequence):
    complement = str.maketrans('ACGTacgt', 'TGCAtgca')
    return sequence.translate(complement)[::-1]

def extract_pattern(sequence, pattern):
    return re.findall(pattern, sequence)

def sort_and_count_sequences(sequences):
    sorted_sequences = sorted(sequences)
    sequence_counts = Counter(sorted_sequences)
    sorted_counts = sorted(sequence_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts

def normalize_counts(counts):
    max_count = max(counts, key=lambda item: item[1])[1]
    normalized = [(seq, count / max_count) for seq, count in counts]
    return normalized

def plot_normalized_counts(normalized_counts, label=None):
    ranks = list(range(1, len(normalized_counts) + 1))
    normalized_values = [count for seq, count in normalized_counts]
    plt.plot(ranks, normalized_values, marker='o', linestyle='None', label=label)

def sequence_analysis_page(page_title, key_prefix, session_state_key):
    st.title(page_title)
    log_memory_usage()
    uploaded_file = st.file_uploader("Upload a FASTQ or FASTQSanger file", type=["fastq", "fastqsanger", "txt"], key=key_prefix)

    if uploaded_file is not None:
        sequence = uploaded_file.getvalue().decode("utf-8").strip()
        search_pattern = st.text_input("Enter the pattern to search for (use '.' for any character):", "GTGCAC...........CTAA.A.A......TACC.GA.", key=f"{key_prefix}_search")
        trimmed_pattern = st.text_input("Trimmed sequences", "CTAA.A.A......TACC", key=f"{key_prefix}_trimmed")

        if st.button('Search Patterns', key=f"{key_prefix}_search_button"):
            reverse_complement = reverse_complement_sequence(sequence)
            matches = extract_pattern(reverse_complement, search_pattern)
            st.write("### Pattern Extraction Results")
            st.write(f"Number of sequences found: {len(matches)}")

            if trimmed_pattern:
                degseq_matches = extract_pattern("\n".join(matches), trimmed_pattern)
                sorted_counts = sort_and_count_sequences(degseq_matches)
                normalized_counts = normalize_counts(sorted_counts)

                st.write("### Sorted Unique Sequences by Frequency")
                col1, col2 = st.columns(2)
                with col1:
                    sorted_counts_text = "\n".join([f"{count:.4f} {seq}" for seq, count in normalized_counts])
                    st.text_area("Normalized Counts", sorted_counts_text, height=400)
                    download_button = st.download_button(label="Download Normalized Counts",
                                                         data=sorted_counts_text,
                                                         file_name="normalized_counts.txt",
                                                         mime="text/plain")
                with col2:
                    plt.figure(figsize=(10, 6))
                    plot_normalized_counts(normalized_counts)
                    plt.xlabel("Rank")
                    plt.ylabel("Normalized Recombination")
                    plt.title("Rank vs Normalized Recombination")
                    st.pyplot(plt)

    log_memory_usage()
    return normalized_counts if uploaded_file else None

# Pages
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["File 1 Analysis", "File 2 Analysis", "File 3 Analysis", "Comparison"])

if page == "File 1 Analysis":
    st.session_state.file1_counts = sequence_analysis_page("File 1 Analysis", "file1", "file1_counts")
elif page == "File 2 Analysis":
    st.session_state.file2_counts = sequence_analysis_page("File 2 Analysis", "file2", "file2_counts")
elif page == "File 3 Analysis":
    st.session_state.file3_counts = sequence_analysis_page("File 3 Analysis", "file3", "file3_counts")
elif page == "Comparison":
    if "file1_counts" in st.session_state and "file2_counts" in st.session_state and "file3_counts" in st.session_state:
        all_counts = st.session_state.file1_counts + st.session_state.file2_counts + st.session_state.file3_counts
        combined_counts = sort_and_count_sequences([seq for seq, count in all_counts])
        normalized_combined = normalize_counts(combined_counts)

        st.write("### Combined Sorted Unique Sequences by Frequency")
        col1, col2 = st.columns(2)
        with col1:
            combined_counts_text = "\n".join([f"{count:.4f} {seq}" for seq, count in normalized_combined])
            st.text_area("Combined Normalized Counts", combined_counts_text, height=400)
            download_button = st.download_button(label="Download Combined Normalized Counts",
                                                 data=combined_counts_text,
                                                 file_name="combined_normalized_counts.txt",
                                                 mime="text/plain")
        with col2:
            plt.figure(figsize=(10, 6))
            plot_normalized_counts(normalized_combined)
            plt.xlabel("Rank")
            plt.ylabel("Normalized Recombination")
            plt.title("Combined Rank vs Normalized Recombination")
            st.pyplot(plt)

    else:
        st.write("Please complete the analyses for File 1, File 2, and File 3 first.")

