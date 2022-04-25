import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
        borderBottomColor: '#bbb',
        borderBottomWidth: 1,
        paddingBottom: 10,
    },
    productContainer: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
        alignItems: 'stretch',
        borderBottomColor: '#bbb',
        borderBottomWidth: 1,
    },
    item: {
        padding: 20,
        fontSize: 18,
    },
    detailsText: {
        fontSize: 18,
        padding: 10,
    },
    lastDetail: {
        marginBottom: 20,
    },
    TouchableHighlight: {
        display: 'flex',
        alignItems: 'center',
    },
});

export default styles;