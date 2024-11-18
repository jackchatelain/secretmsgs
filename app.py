# Import necessary libraries
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
from cryptography.fernet import Fernet

# Define a function to generate a secret key
def generate_key():
    # Generate a secret key using Fernet
    key = Fernet.generate_key()
    return key

# Define a function to encrypt text
def encrypt_text(text, key):
    # Create a Fernet object with the secret key
    fernet = Fernet(key)
    # Encode the text to bytes
    text_bytes = text.encode()
    # Encrypt the text
    encrypted_text = fernet.encrypt(text_bytes)
    # Return the encrypted text as a string
    return encrypted_text.decode()

# Define a function to decrypt text
def decrypt_text(encrypted_text, key):
    # Create a Fernet object with the secret key
    fernet = Fernet(key)
    # Decode the encrypted text from string to bytes
    encrypted_text_bytes = encrypted_text.encode()
    # Decrypt the text
    decrypted_text = fernet.decrypt(encrypted_text_bytes)
    # Return the decrypted text as a string
    return decrypted_text.decode()

# Define the main application class
class Application(Gtk.Application):
    def __init__(self, application_id, flags):
        super().__init__(application_id=application_id, flags=flags)
        self.create_action('generate_key', self.generate_key_callback)
        self.create_action('encrypt', self.encrypt_callback)
        self.create_action('decrypt', self.decrypt_callback)

    def do_activate(self):
        # Create the main window
        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title('Secret Messages 11')
        self.window.set_default_size(800, 500)

        # Create a grid to hold the widgets
        grid = Gtk.Grid()
        grid.set_vexpand(True)
        grid.set_hexpand(True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        self.window.set_child(grid)

        # Create labels for the input fields
        text_label = Gtk.Label(label='Text to Encrypt/Decrypt:')
        key_label = Gtk.Label(label='Secret Key:')

        # Attach labels to the grid
        grid.attach(key_label, 0, 0, 1, 1)
        grid.attach(text_label, 0, 2, 1, 1)

        # Create a text entry for the text to encrypt/decrypt
        self.text_entry = Gtk.Entry()
        self.text_entry.set_placeholder_text('Enter text to encrypt/decrypt')
        grid.attach(self.text_entry, 1, 2, 1, 1)
        self.text_entry.set_hexpand(True)
        self.text_entry.set_margin_top(5)
        self.text_entry.set_margin_bottom(5)
        self.text_entry.set_margin_start(5)
        self.text_entry.set_margin_end(5)
        
        # Create a horizontal box to hold the entry and button
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        # Create a text entry for the secret key
        self.key_entry = Gtk.Entry()
        self.key_entry.set_placeholder_text('Enter secret key')
        hbox.append(self.key_entry)
        self.key_entry.set_hexpand(True)
        self.key_entry.set_margin_top(5)
        self.key_entry.set_margin_bottom(5)
        self.key_entry.set_margin_start(5)
        self.key_entry.set_margin_end(5)

        # Create a button to generate a secret key
        generate_key_button = Gtk.Button(label='Generate Key')
        generate_key_button.set_action_name('app.generate_key')
        hbox.append(generate_key_button)
        generate_key_button.set_margin_top(5)
        generate_key_button.set_margin_bottom(5)
        generate_key_button.set_margin_start(5)
        generate_key_button.set_margin_end(5)
        
        # Attach the horizontal box to the grid
        grid.attach(hbox, 1, 0, 1, 1)
        hbox.set_hexpand(True)

        # Create a horizontal separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 0, 1, 3, 1)
        separator.set_margin_top(10)
        separator.set_margin_bottom(10)

        # Create a button to encrypt the text
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        encrypt_button = Gtk.Button(label='Encrypt')
        encrypt_button.set_action_name('app.encrypt')
        encrypt_button.set_margin_top(5)
        encrypt_button.set_margin_bottom(5)
        encrypt_button.set_margin_start(5)
        encrypt_button.set_margin_end(5)
        hbox2.append(encrypt_button)

        # Create a button to decrypt the text
        decrypt_button = Gtk.Button(label='Decrypt')
        decrypt_button.set_action_name('app.decrypt')
        decrypt_button.set_margin_top(5)
        decrypt_button.set_margin_bottom(5)
        decrypt_button.set_margin_start(5)
        decrypt_button.set_margin_end(5)
        hbox2.append(decrypt_button)
        grid.attach(hbox2, 1, 3, 1, 1)
        hbox2.set_hexpand(True)

        # Create a text view to display the result
        self.result_view = Gtk.TextView()
        self.result_view.set_wrap_mode(Gtk.WrapMode.WORD)  # Enable word wrapping
        grid.attach(self.result_view, 0, 4, 3, 1)
        self.result_view.set_vexpand(True)
        self.result_view.set_hexpand(True)
        self.result_view.set_margin_top(5)
        self.result_view.set_margin_bottom(5)
        self.result_view.set_margin_start(5)
        self.result_view.set_margin_end(5)

        # Show the window
        self.window.present()

    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)

    def generate_key_callback(self, action, param):
        # Generate a secret key and display it in the key entry
        key = generate_key()
        self.key_entry.set_text(key.decode())

    def encrypt_callback(self, action, param):
        # Get the text and key from the entries
        text = self.text_entry.get_text()
        key = self.key_entry.get_text().encode()
        # Encrypt the text
        encrypted_text = encrypt_text(text, key)
        # Display the encrypted text in the result view
        self.result_view.get_buffer().set_text(encrypted_text)

    def decrypt_callback(self, action, param):
        # Get the text and key from the entries
        encrypted_text = self.text_entry.get_text()
        key = self.key_entry.get_text().encode()
        # Decrypt the text
        decrypted_text = decrypt_text(encrypted_text, key)
        # Display the decrypted text in the result view
        self.result_view.get_buffer().set_text(decrypted_text)

# Create the application
application = Application('org.example.TextEncryptor', Gio.ApplicationFlags.FLAGS_NONE)

# Run the application
application.run(None)
