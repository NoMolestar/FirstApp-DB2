import { Button, Text, View } from 'react-native';
import { useEffect, useState } from 'react';
import styles from '../styles/Styles';
import { useIsFocused } from '@react-navigation/native';

const Details = ({navigation, route}) => {

    const [product, setProduct] = useState({});
    const isFocused = useIsFocused();

    const handleClick = () => {
      navigation.navigate("home");
  }

    const getProduct = () => {
        return fetch(`http://localhost:5000/select/${route.params.id}`)
            .then((response) => response.json())
            .then((json) => {
                return json;
            })
            .catch((error) => {
                console.error(error);
            });
    }

    useEffect(() => {
        getProduct().then((data) => setProduct(data));
    }, [isFocused]);

  return (
    <View style={styles.container}>
      <Text style={styles.detailsText}> ID: {product.id} </Text>
      <Text style={styles.detailsText}> Name: {product.name} </Text>
      <Text style={[styles.detailsText, styles.lastDetail]}> Price: ${product.price} </Text>
      <Button title='Go back' color={'red'} onPress={handleClick}></Button>
    </View>
  );
}

export default Details;