import { useIsFocused } from "@react-navigation/native";
import { useEffect, useState, useContext } from "react";
import { FlatList, View, Button } from "react-native";
import Product from "../components/Product";
import axios from "axios";
import GlobalContext from "../utils/GlobalContext";

const Home = ({ navigation }) => {
  const { state, dispatch } = useContext(GlobalContext);
  const [data, setData] = useState([]);
  const isFocused = useIsFocused();

  const logout = () => {
    dispatch({ type: "LOGOUT" });
    navigation.navigate("login");
  };

  const getDataFromAPI = async () => {
    const response = await axios.get("http://localhost:5000/select", {
      headers: {
        Authorization: `${state.email}:${state.password}`,
      },
    });
    setData(response.data);
  };

  useEffect(() => {
    if (!state.email) {
      navigation.navigate("login");
      return;
    }
    getDataFromAPI();
  }, [isFocused]);

  const onDelete = async () => {
    try {
      const response = await axios.delete("http://localhost:5000/delete", {
        id,
      });
      if (response.status === 200) {
        getDataFromAPI();
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      console.log("error: ", error);
    }
  };

  const deletion = () =>
  Alert.alert(
    "Deletion",
    "Are you sure you want to delete this item?",
    [
      {
        text: "Cancel",
        onPress: () => console.log("Cancel Pressed"),
        style: "cancel"
      },
      { text: "OK", onPress: () => onDelete }
    ]
  );

  return (
    <View>
      <FlatList
        data={data}
        renderItem={({ item }) => (
          <View style={{
            flexDirection: "row",
            margin: 20
          }}>
            <Product id={item.id} name={item.name} nav={navigation} />
            <Button onPress={deletion} color={"red"}  title="Delete"/>
          </View>
        )}
      />
      <Button onPress={logout} title="Logout" />
    </View>
  );
};

export default Home;
