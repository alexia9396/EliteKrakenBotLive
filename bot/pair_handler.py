import logging

def get_valid_pairs(kraken):
    """
    Fetches valid trading pairs from Kraken API.
    :param kraken: Kraken API client instance
    :return: List of valid trading pairs
    """
    try:
        response = kraken.query_public('AssetPairs')
        if 'error' in response and response['error']:
            logging.error(f"Kraken API error: {response['error']}")
            return []
        pairs = response.get('result', {})
        valid_pairs = [pair for pair in pairs.keys()]
        return valid_pairs
    except Exception as e:
        logging.error(f"⚠️ Exception during get_valid_pairs() {e}")
        return []
