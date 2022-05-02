import { Button, Text, View } from "react-native";
import { useEffect, useState, useContext } from "react";
import styles from "../styles/Styles";
import { useIsFocused } from "@react-navigation/native";
import axios from "axios";
import GlobalContext from "../utils/GlobalContext";

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

  return (
    <View style={styles.container}>
      <Text style={styles.detailsText}> ID: {product.id} </Text>
      <Text style={styles.detailsText}> Name: {product.name} </Text>
      <Text style={[styles.detailsText, styles.lastDetail]}>
        {" "}
        Price: ${product.price}{" "}
      </Text>
      <Button title="Go back" color={"red"} onPress={handleClick}></Button>
    </View>
  );
};

export default Details;
