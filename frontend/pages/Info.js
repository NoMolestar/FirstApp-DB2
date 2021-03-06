import { Button, Text, View } from "react-native";
import { useEffect, useState, useContext } from "react";
import styles from "../styles/Styles";
import { useIsFocused } from "@react-navigation/native";
import axios from "axios";
import GlobalContext from "../utils/GlobalContext";
import { TextInput } from "react-native-gesture-handler";

const Info = ({ navigation, route }) => {
  const { state } = useContext(GlobalContext);
  const [id, setId] = useState("");
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
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
    const { id, name, price } = response.data;
    setId(id);
    setName(name);
    setPrice(price);
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
      const response = await axios.put(
        `http://localhost:5000/edit/${id}`,
        {
          name,
          price,
        },
        {
          headers: {
            Authorization: `${state.email}:${state.password}`,
          },
        }
      );
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
      <Text style={styles.detailsText}> ID: {id} </Text>
      <Text style={styles.detailsText}> Name: </Text>
      <TextInput style={styles.input} onChangeText={setName} value={name} />
      <Text style={styles.detailsText}> Price: </Text>
      <TextInput style={styles.input} onChangeText={setPrice} value={price} />
      <View
        style={{
          flexDirection: "row",
          margin: 20,
        }}
      >
        <Button title="Go back" color={"red"} onPress={handleClick}></Button>
        <Button title="Update" color={"green"} onPress={onUpdate}></Button>
      </View>
    </View>
  );
};

export default Info;
