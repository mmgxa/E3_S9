from gradio_client import Client

client = Client("http://35.87.211.199")
result = client.predict(
				"Howdy!",	# str  in 'text' Textbox component
                512,
				api_name="/predict"
)
print(result)