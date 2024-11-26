from tqdm import tqdm

def process_file( file ):
	try:
		with open(file, 'r') as f:
			lines = f.readlines()
		# Iterate through the lines with a progress bar
		for n in tqdm(range(len(lines)), desc="Processing lines"):
			line = lines[n]

	except FileNotFoundError:
		print(f"Error: The file '{file}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
	process_file( "OUTCAR" )
