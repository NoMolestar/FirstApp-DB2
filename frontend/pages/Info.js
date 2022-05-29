import { Button, Text, View } from "react-native";
import { useEffect, useState, useContext } from "react";
import styles from "../styles/Styles";
import { useIsFocused } from "@react-navigation/native";
import axios from "axios";
import GlobalContext from "../utils/GlobalContext";
import { TextInput } from "react-native-gesture-handler";

const Details = ({ navigation, route }) => {
  const { state } = useContext(GlobalContext);
  const [product, setProduct] = useState({});
  const isFocused = useIsFocused();

  const handleClick = () => {
    navigation.navigate("home");
  };

  const getProduct = async () => {
    const response = await axios.get(
      `http://localhost:5000/select/${route.params.id}`,
      {
        headers: {
          Authorization: `${state.email}:${state.password}`,
        },
      }
    );
    setProduct(response.data);
    return response.data;
    return fetch(`http://localhost:5000/select/${route.params.id}`)
      .then((response) => response.json())
      .then((json) => {
        return json;
      })
      .catch((error) => {
        console.error(error);
      });
  };

  useEffect(() => {
    if (!state.email) {
      navigation.navigate("login");
      return;
    }
    getProduct();
  }, [isFocused]);

  const onUpdate = async () => {
    try {
      const response = await axios.post("http://localhost:5000/update", {
        id: product.id,
        name: product.name,
        price: product.price,
      });
      if (response.status === 200) {
        navigation.navigate("home");
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      console.log("error: ", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.detailsText}> ID: </Text>
      <TextInput style={styles.detailsText}> {product.id} </TextInput>
      <Text style={styles.detailsText}> Name: </Text>
      <TextInput style={styles.detailsText}> {product.name} </TextInput>
      <Text style={styles.detailsText}> Precio: </Text>
      <TextInput style={[styles.detailsText, styles.lastDetail]}>
        {" "}
        Price: ${product.price}{" "}
      </TextInput>
      <View style={{
        flexDirection: "row",
        margin: 20
      }}>
        <Button title="Go back" color={"red"} onPress={handleClick}></Button>
        <Button title="Go back" color={"red"} onPress={onUpdate}></Button>
      </View>
    </View>
  );
};

export default Details;
