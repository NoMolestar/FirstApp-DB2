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

  return (
    <View>
      <FlatList
        data={data}
        renderItem={({ item }) => (
          <Product id={item.id} name={item.name} nav={navigation} />
        )}
      />
      <Button onPress={logout} title="Logout" />
    </View>
  );
};

export default Home;
