import React, { useState } from 'react';
import { View, Text, Button, Image, TextInput, StyleSheet, Alert, ScrollView } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

export default function App() {
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [detectedObjects, setDetectedObjects] = useState([]);
  const [annotatedImage, setAnnotatedImage] = useState(null); // Armazenar imagem anotada

  // Função para selecionar uma imagem
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  // Função para enviar a imagem e a mensagem ao backend
  const sendRequest = async () => {
    if (!image || !message) {
      Alert.alert('Erro', 'Por favor, selecione uma imagem e insira uma mensagem.');
      return;
    }

    const formData = new FormData();
    formData.append('image', {
      uri: image,
      name: 'image.jpg',
      type: 'image/jpeg',
    });
    formData.append('message', message);

    try {
      const res = await axios.post('https://85dd-2804-14d-e642-8452-494f-8d85-c398-e146.ngrok-free.app/find_object', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResponse(res.data.response); // Resposta principal
      setDetectedObjects(res.data.detected_objects); // Lista de objetos detectados
      setAnnotatedImage(`data:image/jpeg;base64,${res.data.annotated_image}`); // Imagem anotada
    } catch (error) {
      console.error(error);
      Alert.alert('Erro', 'Ocorreu um erro ao processar sua solicitação.');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Encontre Objetos</Text>
      <TextInput
        style={styles.input}
        placeholder="Digite sua mensagem (ex.: Cadê a minha carteira?)"
        value={message}
        onChangeText={setMessage}
      />
      <Button title="Selecionar Imagem" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={styles.image} />}
      <Button title="Enviar" onPress={sendRequest} />
      {response && <Text style={styles.response}>{response}</Text>}
      {annotatedImage && <Image source={{ uri: annotatedImage }} style={styles.image} />}
      {detectedObjects.length > 0 && (
        <View style={styles.objectsContainer}>
          <Text style={styles.subtitle}>Objetos Detectados:</Text>
          {detectedObjects.map((obj, index) => (
            <View key={index} style={styles.objectItem}>
              <Text style={styles.objectText}>
                - {obj.name} (Confiança: {obj.confidence.toFixed(2)})
              </Text>
              {obj.nearby && obj.nearby.length > 0 && (
                <Text style={styles.nearbyText}>
                  Próximo a: {obj.nearby.join(", ")}
                </Text>
              )}
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 50,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    paddingHorizontal: 10,
  },
  image: {
    width: 200,
    height: 200,
    marginVertical: 20,
  },
  response: {
    marginTop: 20,
    fontSize: 18,
    textAlign: 'center',
  },
  objectsContainer: {
    marginTop: 20,
    width: '100%',
  },
  subtitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  objectItem: {
    marginBottom: 10,
  },
  objectText: {
    fontSize: 14,
    marginLeft: 10,
  },
  nearbyText: {
    fontSize: 12,
    marginLeft: 20,
    color: 'gray',
  },
});