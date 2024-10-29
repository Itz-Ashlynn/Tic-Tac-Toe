// Import required libraries
const express = require('express');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Helper function to generate a random string (replace with your own logic)
const generateRandomString = () => {
  return Math.random().toString(36).substring(2, 15);
};

// Route for image enhancement with URL parameter
app.get('/api/enhancer', async (req, res) => {
  try {
    const url = req.query.url;
    if (!url) {
      return res.status(400).json({ error: 'URL query parameter is required.' });
    }

    // Step 1: Get the token
    const tokenResponse = await axios.post('https://photoaid.com/en/tools/api/tools/token');
    const { token } = tokenResponse.data;

    console.log('Received token:', token);

    // Fetch the image from the provided URL and convert to base64
    const imageResponse = await axios.get(url, { responseType: 'arraybuffer' });
    const base64Image = Buffer.from(imageResponse.data, 'binary').toString('base64');

    // Step 2: Upload the image
    const uploadResponse = await axios.post('https://photoaid.com/en/tools/api/tools/upload', {
      base64: base64Image,
      token,
      reqURL: '/ai-image-enlarger/upload'
    }, {
      headers: {
        'Cookie': `uuidtoken2=${token};`,
        'Accept-Language': 'en-US',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://photoaid.com',
        'Referer': 'https://photoaid.com/en/tools/ai-image-enlarger',
      }
    });

    const { request_id } = uploadResponse.data;
    console.log('Received request_id:', request_id);

    // Step 3: Check the result
    let statusResponse;
    do {
      statusResponse = await axios.post('https://photoaid.com/en/tools/api/tools/result', {
        request_id,
        reqURL: '/ai-image-enlarger/result'
      }, {
        headers: {
          'Cookie': `uuidtoken2=${token};`,
          'Accept-Language': 'en-US',
          'Content-Type': 'text/plain;charset=UTF-8',
          'Accept': '*/*',
          'Origin': 'https://photoaid.com',
          'Referer': 'https://photoaid.com/en/tools/ai-image-enlarger',
        }
      });

      console.log('Status response:', statusResponse.data);
      await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
    } while (statusResponse.data.statusAPI !== 'ready');

    const resultBase64 = statusResponse.data.result;

    // Save the image temporarily
    const tempImagePath = path.join(__dirname, 'temp_image.jpg');
    fs.writeFileSync(tempImagePath, Buffer.from(resultBase64, 'base64'));

    // Upload the image to imgbb
    const formData = new FormData();
    formData.append('source', fs.createReadStream(tempImagePath));
    formData.append('type', 'file');
    formData.append('action', 'upload');
    formData.append('timestamp', Date.now().toString());
    formData.append('auth_token', generateRandomString()); // Replace with your actual token generation logic

    const uploadImageResponse = await axios.post('https://imgbb.com/json', formData, {
      headers: formData.getHeaders(),
    });

    fs.unlinkSync(tempImagePath); // Delete the temporary file

    if (uploadImageResponse.data.status_txt === 'OK') {
      const imageUrl = uploadImageResponse.data.image.url;
      res.json({
        status: 'success',
        image: imageUrl,
      });
    } else {
      res.status(500).json({ error: 'Image upload failed.' });
    }

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'An error occurred while processing the image.' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
