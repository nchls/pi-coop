import React from 'react';
import { atom, useRecoilValue } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './door.scss';


export const doorState = atom({
	key: 'door',
	default: {
		fetched: false,
		doorStatus: undefined,
		isAutoOpenCloseEnabled: undefined,
		closingTime: undefined
	},
});

const Door = () => {
	useAPIPoll(doorState, '/door/status', 60000);
	const door = useRecoilValue(doorState);
	
	return (
		<div className="door-status">
			<p>Status: { door.doorStatus }</p>
			<p>isAutoOpenCloseEnabled: { door.isAutoOpenCloseEnabled + '' }</p>
			<p>Closing time: { door.closingTime }</p>
		</div>
	);
};

export default Door;