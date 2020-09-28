import React, { useEffect } from 'react';
import { useRecoilState } from 'recoil';


export const useAPIPoll = (atom, endpoint, pollInterval) => {
	const [data, setter] = useRecoilState(atom);
	useEffect(() => {
		const update = () => {
			const response = window.fetch(endpoint)
				.then((response) => response.json())
				.then((response) => {
					setter({
						...data,
						...response,
						fetched: true
					});
				});
		};
		update();
		const interval = setInterval(update, pollInterval);
		return () => {
			clearInterval(interval);
		};
	}, []);
};