#!/usr/bin/env python3

# This script automates the process of generating commit messages using GPT-4

import sys
import subprocess
import requests
import os

# This is the initial prompt that is sent to chatgpt
INITIAL_PROMPT = """
	You are a helpful assistant.
	Your task is to help the user write a good commit message.

	You will receive a summary of git log as first message from the user,
	a summary of git diff as the second message from the user
	and an optional hint for the commit message as the third message of the user.

	Take the whole conversation in consideration and suggest a good commit message.
	Never say anything that is not your proposed commit message, never appologize.

	- Use imperative
	- One line only
	- Be clear and concise
	- Follow standard commit message conventions
	- Do not put message in quotes

	Always provide only the commit message as answer.
"""

# Number of choices chatgpt will provide
NUM_CHOICES = 3

# OpenAI API key
API_KEY=os.getenv('OPENAI_API_KEY')

# Limit the number of lines in git log summary
GIT_LOG_LIMIT=10

# Limit the number of lines per file and total number of lines in git diff summary
GIT_DIFF_LINES_PER_FILE_LIMIT=50
GIT_DIFF_TOTAL_LINES_LIMIT=500

# Main function to interact with the user and process commit messages
def run(messages):
	choices = send_to_chatgpt(messages)
	for choice in choices:
		messages.append({
			'role': 'system',
			'content': choice,
		})

	# Display choices to the user
	print_choices(choices)

	# Get user input
	user_input = input("Choose an option (1-3), type nothing to abort, anything else to continue chat:\n\n> ").lower()

	# If user chose one of the options, create a commit with that message
	if is_integer_in_range(user_input, NUM_CHOICES):
		selected_option = choices[int(user_input) - 1]
		print(f"\nYou selected: {selected_option}\n")
		# Here you can add the logic to commit the message if required
		commit_with_message(selected_option)
		return

	# Abort if nothing was entered
	if user_input == '':
		return

	# Add user input to messages and continue chat
	messages.append({
		'role': 'user',
		'content': user_input,
	})
	run(messages)

# Exception raised when API request fails

# Send messages (including initial prompt and history) to chatgpt and return the choices
def send_to_chatgpt(
	messages,
	api_key=API_KEY,
	num_choices=NUM_CHOICES,
	model='gpt-4'
):
	if not api_key:
		raise NoApiTokenException("Please set your OPENAI_API_KEY environment variable to use the OpenAI API.")

	api_url = 'https://api.openai.com/v1/chat/completions'

	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {api_key}',
	}

	data = {
		'model': model,
		'messages': messages,
		'n': num_choices
	}
	try:
		response = requests.post(api_url, json=data, headers=headers)
		if response.status_code == 200:
			json_response = response.json()
			choices = [choice.get('message', {}).get('content').strip() for choice in json_response.get('choices', [])]
			return choices
		else:
			raise ApiRequestException(response.status_code, response.text)
	except (requests.exceptions.RequestException, ApiRequestException) as e:
		print("\nFailed to send messages to chatgpt:", e)
		retry = input("\nRetry? (y/n):\n\n> ").lower()
		if retry == 'y':
			return send_to_chatgpt(messages, api_key, num_choices, model)
		else:
			print("\nAborting.")
			sys.exit(1)

# Get compact git log output and limit the number of lines
def git_log_summary(max_lines=GIT_LOG_LIMIT):
	try:
		return subprocess.check_output(
			['git', 'log', '--oneline', '-n', str(max_lines)],
			stderr=subprocess.STDOUT,
			text=True
		)
	except subprocess.CalledProcessError as e:
		# If an error occurs, return the stderr output
		# this also happens when there are no commits yet
		return e.output


# Get git diff output and limit the number of lines per file and total number of lines
def git_diff_summary(max_lines_per_file=GIT_DIFF_LINES_PER_FILE_LIMIT, total_max_lines=GIT_DIFF_TOTAL_LINES_LIMIT):
	# Execute git diff and capture the output
	diff_output = subprocess.check_output(['git', 'diff', '--cached'], text=True)
	
	limited_output = []
	current_file_lines = []
	total_lines = 0

	for line in diff_output.split('\n'):
		# Check for start of a new file diff
		if line.startswith("diff --git"):
			# Add current file lines to the limited output if within total max lines
			if total_lines + len(current_file_lines) <= total_max_lines:
				limited_output.extend(current_file_lines)
				total_lines += len(current_file_lines)
			current_file_lines = [line]
		else:
			# Add line to current file if within per file max lines
			if len(current_file_lines) < max_lines_per_file:
				current_file_lines.append(line)

	# Add the last file's lines
	if total_lines + len(current_file_lines) <= total_max_lines:
		limited_output.extend(current_file_lines)

	return '\n'.join(limited_output)

# Function to commit changes in Git with a given message
def commit_with_message(commit_message):
	try:
		subprocess.run(['git', 'commit', '-m', commit_message], check=True)
		print("\nCommit successful.")
	except subprocess.CalledProcessError as e:
		print("\nFailed to commit:", e)

# Utility function to validate if a string is an integer within a specified range
def is_integer_in_range(string, n):
	try:
		number = int(string)  # Convert string to integer
		return 1 <= number <= n  # Check if number is between 1 and n
	except ValueError:
		return False # Return False if conversion to int fails
	
# Function to print choices to the user
def print_choices(choices):
	print("") # Blank lines for readability
	for i, option in enumerate(choices, 1):
		print(f"{i}. {option}")
	print("")

# Exception raised when no API key is provided
class NoApiTokenException(Exception):
	pass

# Exception raised when API request fails
class ApiRequestException(Exception):
	def __init__(self, status_code, response):
		self.status_code = status_code
		self.response = response

def main():
	# Get git log summary:
	git_log = git_log_summary()
	# Get git diff summary:
	git_diff = git_diff_summary()

	messages = [
		{
			'role': 'system',
			'content': INITIAL_PROMPT,
		},
		{
			'role': 'user',
			'content': 'The git log summary is:\n' + git_log,
		},
		{
			'role': 'user',
			'content': 'The git diff summary is:\n' + git_diff,
		},
	]
	if len(sys.argv) >= 2:
		messages.append({
			'role': 'user',
			'content': sys.argv[1],
		})
	run(messages)

if __name__ == "__main__":
	if not API_KEY:
		print("Please set your OPENAI_API_KEY environment variable to use the OpenAI API.")
		sys.exit(1)
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print("") # Blank line for readability
		sys.exit()