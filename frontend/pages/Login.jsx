import { useState, useContext, useEffect } from "react";
import { Button, View, Text, TextInput } from "react-native";
import axios from "axios";
import GlobalContext from "../utils/GlobalContext";

export default function Login({ navigation }) {
  const { state, dispatch } = useContext(GlobalContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (state.email) {
      navigation.navigate("home");
      return;
    }
  }, []);

  const onSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:5000/login", {
        email,
        password,
      });
      if (response.status === 200) {
        dispatch({ type: "LOGIN", email, password });
        navigation.navigate("home");
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      console.log("error: ", error);
    }
  };

  return (
    <View
      style={{
        padding: "1rem",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        rowGap: "1rem",
      }}
    >
      <View
        style={{
          width: "50rem",
          display: "flex",
          rowGap: "2rem",
        }}
      >
        <Text
          style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "1rem" }}
        >
          Log In
        </Text>
        <View style={{ display: "flex", rowGap: "1rem" }}>
          {error && (
            <Text
              style={{
                padding: "2rem",
                color: "red",
                border: "1px solid lightgrey",
              }}
            >
              {error}
            </Text>
          )}
          <View style={{ display: "flex" }}>
            <Text>Email</Text>
            <TextInput
              onChangeText={(text) => setEmail(text)}
              style={{ backgroundColor: "lightgray", padding: "0.5rem" }}
              placeholder="example@mail.com"
            />
          </View>
          <View style={{ display: "flex" }}>
            <Text>Password</Text>
            <TextInput
              onChangeText={(text) => setPassword(text)}
              style={{
                backgroundColor: "lightgray",
                padding: "0.5rem",
                letterSpacing: "0.5rem",
              }}
              placeholder="********"
            />
          </View>
          <Button color="#20B2AA" title="Log In" onPress={onSubmit} />
        </View>
        <Button
          color="#4682B4"
          onPress={() => navigation.navigate("signup")}
          title="Sign Up"
        />
      </View>
    </View>
  );
}
